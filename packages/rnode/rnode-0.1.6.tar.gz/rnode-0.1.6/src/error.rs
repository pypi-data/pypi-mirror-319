use std::fmt;

#[derive(Debug)]
pub enum MarketDataError {
    WebSocketError(String),
    ParseError(String),
    InvalidData(String),
    TimeError(String),
}

impl std::error::Error for MarketDataError {}

impl fmt::Display for MarketDataError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            MarketDataError::WebSocketError(msg) => write!(f, "WebSocket error: {}", msg),
            MarketDataError::ParseError(msg) => write!(f, "Parse error: {}", msg),
            MarketDataError::InvalidData(msg) => write!(f, "Invalid data: {}", msg),
            MarketDataError::TimeError(msg) => write!(f, "Time error: {}", msg),
        }
    }
}

pub type Result<T> = std::result::Result<T, MarketDataError>; 