from dataclasses import dataclass
from .models import Account


@dataclass
class RiskLimits:
    max_position_value: float = 25_000.0
    max_daily_loss: float = 2_000.0
    max_symbol_weight: float = 0.35


def validate_order(account: Account, symbol: str, side: str, quantity: int, price: float, limits: RiskLimits, daily_pnl: float = 0.0) -> tuple[bool, str]:
    if quantity <= 0:
        return False, "Quantity must be positive"
    if price <= 0:
        return False, "Price must be positive"
    if daily_pnl <= -abs(limits.max_daily_loss):
        return False, "Daily loss limit reached"

    current = account.positions.get(symbol)
    current_qty = current.quantity if current else 0
    projected = current_qty + quantity if side.lower() == "buy" else current_qty - quantity
    if projected < 0:
        return False, "Cannot short in long-only mode"
    if projected * price > limits.max_position_value:
        return False, "Maximum position value exceeded"
    return True, "Accepted"
