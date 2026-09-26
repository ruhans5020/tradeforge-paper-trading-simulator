# Execution Model

TradeForge uses a small market-microstructure model to make paper fills less idealized.

### Spread

A configurable spread in basis points is split around the observed market price. Buys cross upward and sells cross downward.

### Slippage

An additional configurable basis-point adjustment is applied in the trade direction.

### Commissions

A per-share commission is charged on each fill and recorded separately from trading P&L.

### Volume constraints

Each bar exposes only a configurable fraction of its reported volume to the simulator. This allows large orders to remain partially filled instead of assuming unlimited liquidity.

### Order types

- Market: eligible for immediate execution.
- Limit: executes only when the simulated price satisfies the limit.
- Stop: activates after the stop condition and then behaves like a market order.
- Stop-limit: activates after the stop condition and then obeys the limit condition.

These rules are deliberately simplified approximations rather than claims about any specific exchange.
