# TradeForge Architecture

TradeForge separates market data, order modeling, execution, accounting, risk, and presentation so each component can be tested independently.

## Data flow

1. `data.py` loads historical OHLCV data.
2. `dashboard.py` displays market state and accepts simulated orders.
3. `simulator.py` advances the clock bar by bar.
4. `risk.py` validates the order against configured limits.
5. `execution.py` models spread, slippage, commissions, and volume-limited fills.
6. `portfolio.py` updates cash, positions, realized P&L, and commissions.
7. `metrics.py` converts the resulting equity curve into performance statistics.

The architecture intentionally keeps execution logic independent from Streamlit so the simulator can later support command-line experiments and automated tests.
