# TradeForge — Paper Trading Simulator

TradeForge is an educational paper-trading simulator designed to model the mechanics of intraday trading without connecting to a brokerage or placing real orders.

## Features

- Virtual cash and buying power
- Market, limit, stop, and stop-limit orders
- Simulated spread, slippage, commissions, and partial fills
- Long-only positions in the initial version
- Realized and unrealized P&L
- Order lifecycle and trade blotter
- Position sizing and risk limits
- Daily loss and concentration controls
- Stop-loss and take-profit brackets
- Candlestick charts, volume, VWAP, SMA, EMA, and RSI
- Historical replay mode
- Portfolio equity curve and performance statistics
- CSV export
- Automated tests for execution and accounting

## Safety and scope

This project is simulation-only. It does not connect to a brokerage, route live orders, or use real money. Results are educational simulations and should not be interpreted as predictions or investment advice.

## Planned stack

Python, Pandas, NumPy, Plotly, Streamlit, and yfinance.

## Project structure

```text
tradeforge-paper-trading-simulator/
├── app/
│   └── dashboard.py
├── tradeforge/
│   ├── data.py
│   ├── models.py
│   ├── execution.py
│   ├── portfolio.py
│   ├── risk.py
│   ├── metrics.py
│   └── simulator.py
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app/dashboard.py
```
