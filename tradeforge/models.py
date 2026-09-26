from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class OrderType(str, Enum):
    MARKET = "market"
    LIMIT = "limit"
    STOP = "stop"
    STOP_LIMIT = "stop_limit"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PARTIALLY_FILLED = "partially_filled"
    FILLED = "filled"
    CANCELLED = "cancelled"
    REJECTED = "rejected"


@dataclass
class Order:
    symbol: str
    side: str
    quantity: int
    order_type: OrderType = OrderType.MARKET
    limit_price: Optional[float] = None
    stop_price: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    status: OrderStatus = OrderStatus.PENDING
    filled_quantity: int = 0
    average_fill_price: float = 0.0
    reason: str = ""

    @property
    def remaining(self) -> int:
        return max(0, self.quantity - self.filled_quantity)


@dataclass
class Position:
    symbol: str
    quantity: int = 0
    average_cost: float = 0.0
    realized_pnl: float = 0.0

    def market_value(self, price: float) -> float:
        return self.quantity * price

    def unrealized_pnl(self, price: float) -> float:
        return (price - self.average_cost) * self.quantity


@dataclass
class Fill:
    symbol: str
    side: str
    quantity: int
    price: float
    timestamp: datetime = field(default_factory=datetime.utcnow)
    commission: float = 0.0
    slippage: float = 0.0


@dataclass
class Account:
    starting_cash: float = 100_000.0
    cash: float = 100_000.0
    realized_pnl: float = 0.0
    commissions: float = 0.0
    fills: list[Fill] = field(default_factory=list)
    positions: dict[str, Position] = field(default_factory=dict)

    def equity(self, prices: dict[str, float]) -> float:
        return self.cash + sum(p.market_value(prices.get(s, p.average_cost)) for s, p in self.positions.items())
