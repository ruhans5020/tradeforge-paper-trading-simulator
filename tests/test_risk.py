from tradeforge.models import Account
from tradeforge.risk import RiskLimits, validate_order


def test_position_limit():
    ok, reason = validate_order(Account(), "AAPL", "buy", 300, 100.0, RiskLimits(max_position_value=25000))
    assert not ok
    assert "position value" in reason
