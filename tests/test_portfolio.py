from tradeforge.models import Account, Fill
from tradeforge.portfolio import apply_fill


def test_buy_then_sell_realizes_pnl():
    account = Account()
    apply_fill(account, Fill("AAPL", "buy", 10, 100.0, commission=1.0))
    apply_fill(account, Fill("AAPL", "sell", 10, 110.0, commission=1.0))
    assert account.positions["AAPL"].quantity == 0
    assert round(account.realized_pnl, 2) == 100.0
    assert round(account.cash, 2) == 100098.0
