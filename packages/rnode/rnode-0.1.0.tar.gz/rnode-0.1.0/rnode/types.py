from typing import Callable, List, Optional
from dataclasses import dataclass
import json

# 回调函数类型
DataCallback = Callable[[str], None]

# 数据状态枚举
class DataStatus:
    BASIC_VALID = "BASIC_VALID"
    EMPTY = "EMPTY"
    INCOMPLETE = "INCOMPLETE"
    INVALID = "INVALID"
    ERROR = "ERROR"

@dataclass
class TotalVolumeData:
    exchange_time: int
    total_volume: float
    taker_buy_volume: float
    number_of_trades: int

@dataclass
class MidPriceData:
    exchange_time: int
    mid_price: float

@dataclass
class KlineData:
    open_time: int
    open: float
    high: float
    low: float
    close: float
    close_time: int

@dataclass
class NodeResponse:
    type: str
    instrument_id: str
    data: Optional[TotalVolumeData | MidPriceData | KlineData]
    status: str
    timestamp: int

    @classmethod
    def from_json(cls, json_str: str) -> 'NodeResponse':
        data = json.loads(json_str)
        return cls(
            type=data["type"],
            instrument_id=data["instrument_id"],
            data=cls._parse_data(data),
            status=data["status"],
            timestamp=data["timestamp"]
        )

    @staticmethod
    def _parse_data(data: dict) -> Optional[TotalVolumeData | MidPriceData | KlineData]:
        if data.get("data") is None:
            return None

        data_type = data["type"]
        data_content = data["data"]

        if data_type == "total_volume":
            return TotalVolumeData(
                exchange_time=data_content["exchange_time"],
                total_volume=data_content["total_volume"],
                taker_buy_volume=data_content["taker_buy_volume"],
                number_of_trades=data_content["number_of_trades"]
            )
        elif data_type == "mid_price":
            return MidPriceData(
                exchange_time=data_content["exchange_time"],
                mid_price=data_content["mid_price"]
            )
        elif data_type == "kline":
            return KlineData(
                open_time=data_content["open_time"],
                open=data_content["open"],
                high=data_content["high"],
                low=data_content["low"],
                close=data_content["close"],
                close_time=data_content["close_time"]
            )
        return None 