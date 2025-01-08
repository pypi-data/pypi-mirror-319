from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal, Optional

import pandas as pd

from finter.data.data_handler.main import DataHandler


@dataclass(slots=True)
class DataConfig:
    position: pd.DataFrame = field(default_factory=pd.DataFrame)
    price: pd.DataFrame = field(default_factory=pd.DataFrame)
    volume: pd.DataFrame = field(default_factory=pd.DataFrame)


@dataclass(slots=True)
class DateConfig:
    start: int = 20150101  # e.g. 20200101
    end: int = int(datetime.now().strftime("%Y%m%d"))  # e.g. 20201231


@dataclass(slots=True)
class CostConfig:
    # unit: basis point
    buy_fee_tax: float = 0.0
    sell_fee_tax: float = 0.0
    slippage: float = 0.0


@dataclass(slots=True)
class ExecutionConfig:
    initial_cash: float = 1e8
    resample_period: Literal[None, "W", "M", "Q"] = None

    rebalancing_method: Literal["auto", "W", "M", "Q", "by_position"] = "auto"

    volume_capacity_ratio: float = 0.0
    market_type: Literal["basic", "id_fund"] = "basic"


@dataclass(slots=True)
class OptionalConfig:
    # todo: currency, seperate dividend
    # adj_dividend: bool = False
    debug: bool = False


@dataclass(slots=True)
class CacheConfig:
    data_handler: Optional[DataHandler] = None
    timeout: int = 300
    maxsize: int = 5


@dataclass(slots=True)
class FrameConfig:
    shape: tuple[int, int] = field(default_factory=tuple)
    common_columns: list[str] = field(default_factory=list)
    common_index: list[str] = field(default_factory=list)


@dataclass(slots=True)
class SimulatorConfig:
    date: DateConfig
    cost: CostConfig
    execution: ExecutionConfig
    optional: OptionalConfig
    cache: CacheConfig
    frame: FrameConfig
