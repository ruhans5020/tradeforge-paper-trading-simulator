from dataclasses import dataclass, field
from datetime import datetime
import pandas as pd
from .execution import ExecutionConfig, simulate_fill
from .models import Account, Order, OrderStatus
from .portfolio import apply_fill
from .risk import RiskLimits, validate_order


@dataclass
class Simulator:
    account: Account = field(default_factory=Account)
    execution: ExecutionConfig = field(default_factory=ExecutionConfig)
    risk: RiskLimits = field(default_factory=RiskLimits)
    orders: list[Order] = field(default_factory=list)
    equity_history: list[dict] = field(default_factory=list)

    def submit(self, order: Order, price: float) -> Order:
        ok, reason = validate_order(self.account, order.symbol, order.side, order.quantity, price, self.risk)
        if not ok:
            order.status = OrderStatus.REJECTED
            order.reason = reason
            self.orders.append(order)
            return order
        self.orders.append(order)
        return order

    def process_bar(self, timestamp, row: pd.Series, volume_fraction: float = 0.10) -> None:
        price = float(row["close"])
        available = max(1, int(float(row.get("volume", 1)) * volume_fraction))
        for order in self.orders:
            if order.status in {OrderStatus.FILLED, OrderStatus.CANCELLED, OrderStatus.REJECTED}:
                continue
            fill = simulate_fill(order, price, available, self.execution)
            if fill:
                apply_fill(self.account, fill)
        prices = {s: price for s in self.account.positions}
        self.equity_history.append({"timestamp": timestamp, "equity": self.account.equity(prices), "cash": self.account.cash})

    def equity_curve(self) -> pd.DataFrame:
        return pd.DataFrame(self.equity_history)

    def reset(self) -> None:
        self.account = Account(starting_cash=self.account.starting_cash, cash=self.account.starting_cash)
        self.orders.clear()
        self.equity_history.clear()
