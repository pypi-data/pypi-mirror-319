use std::sync::Arc;
use tokio::sync::{RwLock, Mutex};
use tokio::time::Duration;
use chrono::Utc;
use crate::error::*;
use crate::ws_client::WsClient;
use crate::types::*;
use crate::utils::*;
use crate::nodes::mid_price::MidPriceNode;
use tracing::error;
use pyo3::prelude::*;
use std::collections::HashMap;
use tokio::sync::broadcast;

pub struct SimpleKlineNode {
    freq: String,
    instruments: HashMap<String, InstrumentData>,
    ws_client: Arc<WsClient>,
    mid_price_nodes: HashMap<String, Arc<MidPriceNode>>,
    kline_sender: Arc<broadcast::Sender<SimpleKlineData>>,
}

#[derive(Clone)]
struct InstrumentData {
    last_exchange_time: Arc<RwLock<i64>>,
    current_data: Arc<RwLock<SimpleKlineData>>,
    interval_manager: Arc<RwLock<IntervalManager>>,
    sending_lock: Arc<Mutex<()>>,
    current_period: Arc<RwLock<i64>>,
}

impl SimpleKlineNode {
    pub fn new(freq: String, instrument_ids: Vec<String>, ws_client: Arc<WsClient>, mid_price_nodes: HashMap<String, Arc<MidPriceNode>>) -> Self {
        let mut instruments = HashMap::new();
        
        // 解析频率获取毫秒数
        let interval_ms = parse_duration(&freq).expect("Invalid frequency");
        
        for instrument_id in instrument_ids {
            instruments.insert(instrument_id.clone(), InstrumentData {
                last_exchange_time: Arc::new(RwLock::new(0)),
                current_data: Arc::new(RwLock::new(SimpleKlineData {
                    open_time: 0,
                    open: 0.0,
                    high: 0.0,
                    low: f64::MAX,
                    close: 0.0,
                    close_time: 0,
                    interval_ms,  // 设置区间长度
                    period_id: 0,
                })),
                interval_manager: Arc::new(RwLock::new(IntervalManager::new(freq.clone())
                    .expect("Invalid frequency"))),
                sending_lock: Arc::new(Mutex::new(())),
                current_period: Arc::new(RwLock::new(0)),
            });
        }
        
        Self {
            freq,
            instruments,
            ws_client,
            mid_price_nodes,
            kline_sender: Arc::new(broadcast::channel(16).0),
        }
    }

    async fn send_data(
        data: &mut SimpleKlineData,
        instrument_id: &str,
        callback: &PyObject,
        current_time: i64,
        sending_lock: &Mutex<()>,
        current_period: &RwLock<i64>,
        period_id: i64,
        kline_sender: &broadcast::Sender<SimpleKlineData>,
    ) -> bool {
        let _lock = sending_lock.lock().await;
        
        let mut period = current_period.write().await;
        if *period >= period_id {
            return false;
        }
        
        if data.close > 0.0 {
            // 发送数据到 resample kline
            if let Err(e) = kline_sender.send(data.clone()) {
                if !e.to_string().contains("no receivers") {
                    error!("Failed to send kline data: {}", e);
                }
            }

            // 发送 JSON 数据到回调
            let response = serde_json::json!({
                "type": "kline",
                "instrument_id": instrument_id,
                "data": {
                    "open_time": data.open_time,
                    "open": data.open,
                    "high": data.high,
                    "low": data.low,
                    "close": data.close,
                    "close_time": data.close_time,
                },
                "status": DataStatus::BasicValid,
                "timestamp": current_time
            });
            
            Python::with_gil(|py| {
                if let Err(e) = callback.call1(py, (serde_json::to_string(&response).unwrap(),)) {
                    error!("Callback failed: {:?}", e);
                }
            });
        } else {
            // 如果没有有效数据，发送 Invalid 状态
            let response = serde_json::json!({
                "type": "kline",
                "instrument_id": instrument_id,
                "data": null,
                "status": DataStatus::Invalid,
                "timestamp": current_time
            });
            
            Python::with_gil(|py| {
                if let Err(e) = callback.call1(py, (serde_json::to_string(&response).unwrap(),)) {
                    error!("Callback failed: {:?}", e);
                }
            });
        }
        
        *period = period_id;
        true
    }

    pub async fn start(&self, callback: PyObject) -> Result<()> {
        // 为每个 instrument 创建订阅
        for (instrument_id, data) in &self.instruments {
            if let Some(mid_price_node) = self.mid_price_nodes.get(instrument_id) {
                let mut price_receiver = mid_price_node.subscribe_price();
                let data_for_price = data.clone();
                let data_for_timer = data.clone();
                let callback_for_price = callback.clone();
                let callback_for_timer = callback.clone();
                let instrument_id_for_price = instrument_id.clone();
                let instrument_id_for_timer = instrument_id.clone();
                let kline_sender_clone = self.kline_sender.clone();  // 克隆 sender

                // 启动价格更新任务
                tokio::spawn(async move {
                    while let Ok((price_instrument_id, mid_price, exchange_time)) = price_receiver.recv().await {
                        
                        if price_instrument_id != instrument_id_for_price {
                            continue;
                        }
                        let exchange_time_ms = exchange_time / 1000;

                        // 检查时间有效性
                        let last_time = *data_for_price.last_exchange_time.read().await;
                        if exchange_time < last_time {
                            continue;  // 跳过过期数据
                        }

                        // 检查交易时间是否超过当前时间
                        let current_time = Utc::now().timestamp_millis();
                        if exchange_time_ms > current_time {
                            continue;  // 跳过未来数据
                        }

                        let mut current = data_for_price.current_data.write().await;
                        let mut manager = data_for_price.interval_manager.write().await;
                        let period_id = manager.get_current_period();
                        
                        // 计算当前周期的时间范围
                        let period_start = period_id * current.interval_ms;
                        let period_end = (period_id + 1) * current.interval_ms - 1;
                        
                        // 检查是否需要发送当前数据
                        if manager.should_advance(exchange_time_ms) {
                            // 如果有数据需要发送
                            if current.open_time > 0 {
                                let sending_lock = data_for_price.sending_lock.clone();
                                let current_period = data_for_price.current_period.clone();
                                
                                if Self::send_data(
                                    &mut current,
                                    &instrument_id_for_price,
                                    &callback_for_price,
                                    current_time,
                                    &sending_lock,
                                    &current_period,
                                    period_id,
                                    &kline_sender_clone,  // 使用克隆的 sender
                                ).await {
                                    manager.advance();
                                    
                                    // 重置数据，但保持 interval_ms
                                    *current = SimpleKlineData {
                                        open_time: 0,
                                        open: 0.0,
                                        high: 0.0,
                                        low: f64::MAX,
                                        close: 0.0,
                                        close_time: 0,
                                        interval_ms: current.interval_ms,
                                        period_id: 0,
                                    };
                                }
                            } else {
                                manager.advance();
                            }
                        }
                        
                        // 更新K线数据
                        if current.open_time == 0 {
                            current.open_time = period_start;
                            current.open = mid_price;
                            current.high = mid_price;
                            current.low = mid_price;
                            current.close = mid_price;
                            current.close_time = period_end;
                            current.period_id = period_id;
                        } else {
                            current.high = current.high.max(mid_price);
                            current.low = current.low.min(mid_price);
                            current.close = mid_price;
                        }
                        
                        *data_for_price.last_exchange_time.write().await = exchange_time;
                    }
                });

                // 启动定时发送任务
                let kline_sender_clone = self.kline_sender.clone();  // 为定时任务克隆 sender
                tokio::spawn(async move {
                    let mut interval = tokio::time::interval(Duration::from_secs(1));
                    loop {
                        interval.tick().await;
                        let current_time = Utc::now().timestamp_millis();
                        
                        let mut manager = data_for_timer.interval_manager.write().await;
                        if manager.should_advance(current_time) {
                            let period_id = manager.get_current_period();
                            let mut current = data_for_timer.current_data.write().await;
                            
                            if Self::send_data(
                                &mut current,
                                &instrument_id_for_timer,
                                &callback_for_timer,
                                current_time,
                                &data_for_timer.sending_lock,
                                &data_for_timer.current_period,
                                period_id,
                                &kline_sender_clone,  // 使用克隆的 sender
                            ).await {
                                manager.advance();
                                
                                // 重置数据，但保持 interval_ms
                                *current = SimpleKlineData {
                                    open_time: 0,
                                    open: 0.0,
                                    high: 0.0,
                                    low: f64::MAX,
                                    close: 0.0,
                                    close_time: 0,
                                    interval_ms: current.interval_ms,
                                    period_id: 0,
                                };
                            }
                        }
                    }
                });
            }
        }

        Ok(())
    }

    pub fn subscribe_kline(&self) -> broadcast::Receiver<SimpleKlineData> {
        let receiver = self.kline_sender.subscribe();
        receiver
    }
} 