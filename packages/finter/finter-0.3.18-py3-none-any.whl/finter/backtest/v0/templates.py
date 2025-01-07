from dataclasses import dataclass
from typing import ClassVar, Dict, Literal

from finter.backtest.v0.builder import SimulatorBuilder


@dataclass
class MarketConfig:
    initial_cash: float
    buy_fee_tax: float
    sell_fee_tax: float
    slippage: float
    market_type: Literal["basic", "id_fund"]
    adj_dividend: bool


@dataclass
class MarketTemplates:
    # Class variable to store all market configurations
    CONFIGS: ClassVar[Dict[str, MarketConfig]] = {
        "kr_stock": MarketConfig(
            initial_cash=100_000_000,  # 1억원
            buy_fee_tax=1.2,
            sell_fee_tax=31.2,
            slippage=10,
            market_type="basic",
            adj_dividend=False,
        ),
        "id_fund": MarketConfig(
            initial_cash=1_000_000_000,
            buy_fee_tax=40,
            sell_fee_tax=50,
            slippage=10,
            market_type="id_fund",
            adj_dividend=False,
        ),
    }

    @classmethod
    def create_simulator(
        cls,
        market_type: Literal["kr_stock", "id_fund"],
    ) -> SimulatorBuilder:
        if market_type not in cls.CONFIGS:
            raise ValueError(f"Unsupported market type: {market_type}")

        config = cls.CONFIGS[market_type]
        return (
            SimulatorBuilder()
            .update_cost(
                buy_fee_tax=config.buy_fee_tax,
                sell_fee_tax=config.sell_fee_tax,
                slippage=config.slippage,
            )
            .update_execution(
                initial_cash=config.initial_cash,
                market_type=config.market_type,
            )
        )
