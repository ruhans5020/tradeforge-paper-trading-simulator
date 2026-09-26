# Simulation Limitations

TradeForge is not an exchange simulator. It approximates execution mechanics for educational research.

Important limitations include:

- Historical OHLCV data does not contain the full order book.
- The spread and slippage model is configurable but simplified.
- Partial fills use a volume-fraction heuristic rather than exchange matching.
- Stop orders are triggered from the available bar price rather than tick-level market data.
- Market-hours and overnight rules are not yet modeled at exchange-calendar precision.
- The current portfolio engine is long-only.
- Historical data can contain revisions, missing observations, and provider-specific constraints.
- Performance metrics are descriptive of the simulation and are not forecasts.
