from dataclasses import dataclass
import math
from .models import Fill, Order, OrderStatus, OrderType


@dataclass
class ExecutionConfig:
    commission_per_share: float = 0.005
    spread_bps: float = 2.0
    slippage_bps: float = 3.0
    max_fill_fraction: float = 1.0


def simulate_fill(order: Order, last_price: float, available_volume: int, cfg: ExecutionConfig) -> Fill | None:
    """Apply a simplified, deterministic market microstructure model."""
    if order.remaining <= 0 or order.status in {OrderStatus.CANCELLED, OrderStatus.REJECTED}:
        return None

    side = order.side.lower()
    side_sign = 1 if side == "buy" else -1

    if order.order_type in {OrderType.STOP, OrderType.STOP_LIMIT}:
        if order.stop_price is None:
            order.status = OrderStatus.REJECTED
            order.reason = "Stop order requires a stop price"
            return None
        triggered = last_price >= order.stop_price if side == "buy" else last_price <= order.stop_price
        if not triggered:
            return None
        # Once triggered, a stop becomes a market order or a limit order.
        effective_type = OrderType.LIMIT if order.order_type == OrderType.STOP_LIMIT else OrderType.MARKET
    else:
        effective_type = order.order_type

    half_spread = last_price * cfg.spread_bps / 20_000
    base = last_price + side_sign * half_spread

    if effective_type == OrderType.LIMIT:
        if order.limit_price is None:
            order.status = OrderStatus.REJECTED
            order.reason = "Limit order requires a limit price"
            return None
        if side == "buy" and base > order.limit_price:
            return None
        if side == "sell" and base < order.limit_price:
            return None
        base = min(base, order.limit_price) if side_sign > 0 else max(base, order.limit_price)

    slip = base * cfg.slippage_bps / 10_000
    price = base + side_sign * slip
    qty = min(order.remaining, max(0, math.floor(available_volume * cfg.max_fill_fraction)))
    if qty <= 0:
        return None

    commission = qty * cfg.commission_per_share
    order.filled_quantity += qty
    prior = order.average_fill_price * (order.filled_quantity - qty)
    order.average_fill_price = (prior + price * qty) / order.filled_quantity
    order.status = OrderStatus.FILLED if order.remaining == 0 else OrderStatus.PARTIALLY_FILLED

    return Fill(
        order.symbol,
        side,
        qty,
        price,
        commission=commission,
        slippage=abs(price - last_price) * qty,
    )
