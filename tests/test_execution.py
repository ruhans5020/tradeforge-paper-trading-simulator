from tradeforge.execution import ExecutionConfig, simulate_fill
from tradeforge.models import Order, OrderType, OrderStatus


def test_market_order_fills():
    order = Order("AAPL", "buy", 10, OrderType.MARKET)
    fill = simulate_fill(order, 100.0, 1000, ExecutionConfig())
    assert fill is not None
    assert order.status == OrderStatus.FILLED
    assert fill.quantity == 10
    assert fill.price > 100


def test_limit_buy_waits_when_market_above_limit():
    order = Order("AAPL", "buy", 10, OrderType.LIMIT, limit_price=99.0)
    fill = simulate_fill(order, 100.0, 1000, ExecutionConfig())
    assert fill is None
    assert order.status == OrderStatus.PENDING
