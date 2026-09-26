from .models import Account, Fill, Position


def apply_fill(account: Account, fill: Fill) -> None:
    position = account.positions.setdefault(fill.symbol, Position(fill.symbol))
    qty = fill.quantity
    price = fill.price
    commission = fill.commission

    if fill.side.lower() == "buy":
        total_cost = position.average_cost * position.quantity + price * qty
        position.quantity += qty
        position.average_cost = total_cost / position.quantity
        account.cash -= price * qty + commission
    elif fill.side.lower() == "sell":
        if qty > position.quantity:
            raise ValueError("Long-only simulator cannot sell more than the current position")
        pnl = (price - position.average_cost) * qty
        position.quantity -= qty
        position.realized_pnl += pnl
        account.realized_pnl += pnl
        account.cash += price * qty - commission
        if position.quantity == 0:
            position.average_cost = 0.0
    else:
        raise ValueError("Side must be buy or sell")

    account.commissions += commission
    account.fills.append(fill)
