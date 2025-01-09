use crate::types::*;
use crate::error::Result;
use async_trait::async_trait;
use std::sync::Arc;
use parking_lot::RwLock;

#[async_trait]
pub trait DataNode<T: Clone + Send + Sync + 'static> {
    async fn process_data(&self, data: &str) -> Result<NodeResponse<T>>;
    
    #[allow(unused)]
    fn get_freq(&self) -> &str;
    
    #[allow(unused)]
    fn get_instrument_id(&self) -> &str;
    
    #[allow(unused)]
    fn reset(&self);
}

pub struct BaseNode<T> {
    pub freq: String,
    pub instrument_id: String,
    pub last_exchange_time: Arc<RwLock<i64>>,
    pub current_data: Arc<RwLock<T>>,
} 