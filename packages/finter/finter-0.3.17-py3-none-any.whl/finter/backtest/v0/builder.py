import warnings
from dataclasses import dataclass, field
from typing import Literal, Optional

import numpy as np
import pandas as pd

from finter.backtest.v0.config import (
    CacheConfig,
    CostConfig,
    DataConfig,
    DateConfig,
    ExecutionConfig,
    FrameConfig,
    OptionalConfig,
    SimulatorConfig,
)
from finter.backtest.v0.simulators.base import BaseBacktestor
from finter.backtest.v0.simulators.basic import BasicBacktestor
from finter.backtest.v0.simulators.id_fund import IDFundBacktestor
from finter.backtest.v0.simulators.vars import InputVars
from finter.data.data_handler.main import DataHandler
from finter.modeling.utils import daily2period, get_rebalancing_mask

POSITION_SCALAR = 1e8
BASIS_POINT_SCALAR = 10000


@dataclass
class SimulatorBuilder:
    data: DataConfig = field(default_factory=DataConfig)

    date: DateConfig = field(default_factory=DateConfig)
    cost: CostConfig = field(default_factory=CostConfig)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)
    optional: OptionalConfig = field(default_factory=OptionalConfig)
    cache: CacheConfig = field(default_factory=CacheConfig)
    frame: FrameConfig = field(default_factory=FrameConfig)

    def build(self, position: pd.DataFrame) -> BaseBacktestor:
        from datetime import datetime

        start_date = datetime.strptime(str(self.date.start), "%Y%m%d")
        end_date = datetime.strptime(str(self.date.end), "%Y%m%d")
        position = position.loc[start_date:end_date]

        if position.empty or self.data.price.empty:
            raise ValueError("Both position and price data are required")

        if not (self.date.start < self.date.end):
            raise ValueError("Start date must be earlier than end date")

        data_config = self.__build_data(position)
        self.frame = self.__build_frame(data_config)
        config = self.__build_config()
        input_vars = self.__build_input_vars(config, data_config)

        if self.execution.market_type == "basic":
            return BasicBacktestor(config, input_vars)
        elif self.execution.market_type == "id_fund":
            return IDFundBacktestor(config, input_vars)
        else:
            raise ValueError(f"Unknown market type: {self.execution.market_type}")

    def __build_input_vars(
        self, config: SimulatorConfig, data_config: DataConfig
    ) -> InputVars:
        weight, price = DataProcessor.preprocess_position(config, data_config)
        volume_capacity = DataProcessor.preprocess_volume_capacity(config, data_config)
        rebalancing_mask = DataProcessor.preprocess_rebalancing_mask(
            config, data_config
        )

        buy_price = price * (1 + self.cost.slippage)
        sell_price = price * (1 - self.cost.slippage)

        return InputVars(
            weight=weight,
            price=price,
            buy_price=buy_price,
            sell_price=sell_price,
            volume_capacity=volume_capacity,
            rebalancing_mask=rebalancing_mask,
        )

    def __build_frame(self, data_config: DataConfig) -> FrameConfig:
        return FrameConfig(
            shape=data_config.price.shape,
            common_columns=data_config.position.columns.intersection(
                data_config.price.columns
            ).tolist(),
            common_index=data_config.price.index.tolist(),
        )

    def __build_config(self) -> SimulatorConfig:
        return SimulatorConfig(
            date=self.date,
            cost=self.cost,
            execution=self.execution,
            optional=self.optional,
            cache=self.cache,
            frame=self.frame,
        )

    def __build_data(
        self,
        position: pd.DataFrame,
    ) -> DataConfig:
        def _filter_nonzero_and_common_columns(
            position: pd.DataFrame, price: pd.DataFrame
        ) -> tuple[pd.DataFrame, pd.DataFrame]:
            non_zero_columns = position.columns[position.sum() != 0]
            position = position[non_zero_columns]
            price = price[non_zero_columns]

            common_columns = position.columns.intersection(price.columns)
            if len(common_columns) == 0:
                raise ValueError("No overlapping columns between position and price")

            position = position[common_columns]
            price = price[common_columns]

            return position, price

        def _align_index_with_price(
            position: pd.DataFrame, price: pd.DataFrame
        ) -> tuple[pd.DataFrame, pd.DataFrame, pd.Timestamp]:
            start_date = (
                (position.shift(-1).notna() * price.notna()).any(axis=1).idxmax()
            )

            position = position.loc[start_date:]
            price = price.loc[start_date:]
            position_start_date = position.index.min()

            if price.loc[:position_start_date].empty:
                warnings.warn(
                    "No price data before position start date. "
                    "Position data will be trimmed to match available price data.",
                    UserWarning,
                )
                price_start_date = price.index[0]
            else:
                price_start_date = price.loc[:position_start_date].index[-1]

            common_end_date = min(position.index[-1], price.index[-1])
            price = price.loc[price_start_date:common_end_date]
            position = position.reindex(price.index)

            return position, price, price_start_date

        # Initialize variables
        price = self.data.price
        volume = self.data.volume

        if not position.empty and not price.empty:
            position, price = _filter_nonzero_and_common_columns(position, price)
            position, price, price_start_date = _align_index_with_price(position, price)

            if not volume.empty:
                volume = volume.loc[price_start_date:]
                volume = volume[position.columns]
                volume = volume.reindex(position.index).loc[: position.index[-1]]

        return DataConfig(position=position, price=price, volume=volume)

    def update_data(
        self,
        price: Optional[pd.DataFrame] = None,
        volume: Optional[pd.DataFrame] = None,
    ) -> "SimulatorBuilder":
        price = price if price is not None else self.data.price
        volume = volume if volume is not None else self.data.volume
        self.data = DataConfig(price=price, volume=volume)
        return self

    def update_date(
        self, start: Optional[int] = None, end: Optional[int] = None
    ) -> "SimulatorBuilder":
        self.date = DateConfig(
            start=start if start is not None else self.date.start,
            end=end if end is not None else self.date.end,
        )
        return self

    def update_cost(
        self,
        buy_fee_tax: Optional[float] = None,
        sell_fee_tax: Optional[float] = None,
        slippage: Optional[float] = None,
    ) -> "SimulatorBuilder":
        buy_fee_tax = (
            buy_fee_tax / BASIS_POINT_SCALAR
            if buy_fee_tax is not None
            else self.cost.buy_fee_tax
        )
        sell_fee_tax = (
            sell_fee_tax / BASIS_POINT_SCALAR
            if sell_fee_tax is not None
            else self.cost.sell_fee_tax
        )
        slippage = (
            slippage / BASIS_POINT_SCALAR
            if slippage is not None
            else self.cost.slippage
        )

        self.cost = CostConfig(
            buy_fee_tax=buy_fee_tax,
            sell_fee_tax=sell_fee_tax,
            slippage=slippage,
        )
        return self

    def update_execution(
        self,
        initial_cash: Optional[float] = None,
        resample_period: Optional[Literal[None, "W", "M", "Q"]] = None,
        rebalancing_method: Optional[
            Literal["auto", "W", "M", "Q", "by_position"]
        ] = None,
        volume_capacity_ratio: Optional[float] = None,
        market_type: Optional[Literal["basic", "id_fund"]] = None,
    ) -> "SimulatorBuilder":
        # Create new rebalancing config with updated values

        self.execution = ExecutionConfig(
            initial_cash=initial_cash
            if initial_cash is not None
            else self.execution.initial_cash,
            resample_period=resample_period
            if resample_period is not None
            else self.execution.resample_period,
            rebalancing_method=rebalancing_method
            if rebalancing_method is not None
            else self.execution.rebalancing_method,
            volume_capacity_ratio=volume_capacity_ratio
            if volume_capacity_ratio is not None
            else self.execution.volume_capacity_ratio,
            market_type=market_type
            if market_type is not None
            else self.execution.market_type,
        )

        return self

    def update_optional(self, debug: Optional[bool] = None) -> "SimulatorBuilder":
        self.optional = OptionalConfig(
            debug=debug if debug is not None else self.optional.debug,
        )
        return self

    def update_cache(
        self,
        data_handler: Optional[DataHandler] = None,
        timeout: Optional[int] = None,
        maxsize: Optional[int] = None,
    ) -> "SimulatorBuilder":
        self.cache = CacheConfig(
            data_handler=data_handler
            if data_handler is not None
            else self.cache.data_handler,
            timeout=timeout if timeout is not None else self.cache.timeout,
            maxsize=maxsize if maxsize is not None else self.cache.maxsize,
        )
        return self

    def update(self, **kwargs) -> "SimulatorBuilder":
        """
        Update any configuration options in a single call.
        Uses __slots__ from Config classes to determine which parameters belong where.

        Raises:
            ValueError: If an unknown parameter is provided
        """
        updates = {
            "data": {},
            "date": {},
            "cost": {},
            "execution": {},
            "optional": {},
            "cache": {},
        }

        # Track unknown parameters
        unknown_params = []

        # Sort parameters into their respective config updates
        for key, value in kwargs.items():
            if key in DataConfig.__slots__:
                updates["data"][key] = value
            elif key in DateConfig.__slots__:
                updates["date"][key] = value
            elif key in CostConfig.__slots__:
                updates["cost"][key] = value
            elif key in ExecutionConfig.__slots__:
                updates["execution"][key] = value
            elif key in OptionalConfig.__slots__:
                updates["optional"][key] = value
            elif key in CacheConfig.__slots__:
                updates["cache"][key] = value
            else:
                unknown_params.append(key)

        # Raise error if unknown parameters were provided
        if unknown_params:
            raise ValueError(
                f"Unknown parameter(s): {', '.join(unknown_params)}. "
                "Please check the parameter names and try again."
            )

        # Apply updates only if there are changes
        if updates["data"]:
            self.update_data(**updates["data"])
        if updates["date"]:
            self.update_date(**updates["date"])
        if updates["cost"]:
            self.update_cost(**updates["cost"])
        if updates["execution"]:
            self.update_execution(**updates["execution"])
        if updates["optional"]:
            self.update_optional(**updates["optional"])
        if updates["cache"]:
            self.update_cache(**updates["cache"])

        return self


class DataProcessor:
    def __init__(self):
        pass

    @staticmethod
    def preprocess_position(config: SimulatorConfig, data: DataConfig):
        if config.execution.resample_period:
            position = daily2period(
                data.position,
                config.execution.resample_period,
                keep_index=True,
            )
        else:
            position = data.position

        return (
            (position / POSITION_SCALAR).to_numpy(),
            data.price.to_numpy(),
        )

    @staticmethod
    def preprocess_volume_capacity(config: SimulatorConfig, data: DataConfig):
        if config.execution.volume_capacity_ratio == 0:
            volume = pd.DataFrame(
                np.inf,
                index=config.frame.common_index,
                columns=config.frame.common_columns,
            )
            return volume.to_numpy()
        else:
            volume = data.volume.reindex(
                config.frame.common_index,
                columns=config.frame.common_columns,
            )
            return volume.fillna(0).to_numpy() * config.execution.volume_capacity_ratio

    @staticmethod
    def preprocess_rebalancing_mask(config: SimulatorConfig, data: DataConfig):
        period = config.execution.rebalancing_method
        if period in ["W", "M", "Q"]:
            return np.array(
                [
                    d in get_rebalancing_mask(data.position, period)  # type: ignore
                    for d in config.frame.common_index
                ],
                dtype=int,
            )
        else:
            return np.array([])


if __name__ == "__main__":
    from finter.data import ContentFactory, ModelData

    start, end = 20220101, 20240101
    position = ModelData.load("alpha.krx.krx.stock.ldh0127.div_new_1").loc["2022"]
    price = ContentFactory("kr_stock", start, end).get_df("price_close", fill_nan=False)

    builder = SimulatorBuilder()

    (
        builder.update_data(price=price)
        .update_date(start=20240101, end=20240131)
        .update_cost(buy_fee_tax=10, sell_fee_tax=10, slippage=10)
        .update_execution(initial_cash=1e4, market_type="basic")
        .update_optional(debug=True)
    )

    res = []
    for rebalancing_method in [
        "auto",
        "W",
        "M",
        "Q",
        "by_position",
    ]:
        builder.update_execution(rebalancing_method=rebalancing_method)

        simulator = builder.build(position)
        res.append(simulator.run())
