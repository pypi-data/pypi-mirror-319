use chrono::{Datelike, TimeZone, Utc};

pub struct IntervalManager {
    freq: String,
    current_index: i64,  // 当前周期索引
    duration_ms: i64,    // 周期长度（毫秒）
}

impl IntervalManager {
    pub fn new(freq: String) -> Option<Self> {
        let duration_ms = parse_duration(&freq)?;
        let now = Utc::now().timestamp_millis();
        let current_index = now / duration_ms;
        
        Some(Self {
            freq,
            current_index,
            duration_ms,
        })
    }

    pub fn get_current_interval(&self) -> (i64, i64) {
        let start = self.current_index * self.duration_ms;
        let end = start + self.duration_ms;
        (start, end)
    }

    pub fn advance(&mut self) {
        self.current_index += 1;
    }

    pub fn should_advance(&self, timestamp: i64) -> bool {
        let (_, current_end) = self.get_current_interval();
        timestamp >= current_end
    }

    pub fn get_current_period(&self) -> i64 {
        self.current_index
    }

    pub fn get_period_id(&self, timestamp: i64) -> i64 {
        timestamp / self.duration_ms
    }

    pub fn get_duration_ms(&self) -> i64 {
        self.duration_ms
    }
}

pub fn get_interval_bounds(freq: &str) -> Option<(i64, i64)> {
    // 获取当前 UTC 时间
    let now = Utc::now();
    
    // 获取当天的开始时间 (UTC 00:00:00)
    let day_start = Utc
        .with_ymd_and_hms(now.year(), now.month(), now.day(), 0, 0, 0)
        .single()?
        .timestamp_millis();
    
    // 计算区间长度（毫秒）
    let duration_ms = parse_duration(freq)?;
    
    // 计算从当天开始到当前时间有多少个完整区间
    let current_ms = now.timestamp_millis();
    let intervals = (current_ms - day_start) / duration_ms;
    
    // 计算区间的开始时间
    let interval_start = day_start + (intervals * duration_ms);
    
    // 计算区间的结束时间
    let next_interval_start = interval_start + duration_ms;
    
    // 获取第二天的开始时间
    let next_day_start = day_start + 24 * 60 * 60 * 1000;
    
    // 如果下一个区间的开始时间超过了当天，使用当天的最后一毫秒
    let interval_end = if next_interval_start > next_day_start {
        next_day_start - 1  // 23:59:59.999
    } else {
        next_interval_start
    };
    
    Some((interval_start, interval_end))
}

pub fn parse_duration(freq: &str) -> Option<i64> {
    let len = freq.len();
    if len < 2 {
        return None;
    }

    let (num_str, unit) = freq.split_at(len - 1);
    let num: i64 = num_str.parse().ok()?;

    match unit {
        "s" => Some(num * 1000),           // 秒转毫秒
        "m" => Some(num * 60 * 1000),      // 分钟转毫秒
        "h" => Some(num * 3600 * 1000),    // 小时转毫秒
        "d" => Some(num * 86400 * 1000),   // 天转毫秒
        _ => None,
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_interval_bounds() {
        // 设置一个固定的当前时间用于测试
        let now = Utc::now();
        let (start, end) = get_interval_bounds("5m").unwrap();
        
        // 验证区间是否正确
        assert!(start <= now.timestamp_millis());
        assert!(end > now.timestamp_millis());
        assert_eq!((end - start) / 1000 / 60, 5); // 应该是 5 分钟
        
        // 测试跨天的情况
        let end_of_day = now.date_naive().and_hms_opt(23, 59, 0).unwrap();
        let (start, end) = get_interval_bounds("5m").unwrap();
        assert!(end <= end_of_day.timestamp_millis() + 999);
    }
} 