import streamlit as st
import plotly.graph_objects as go
from tradeforge.data import add_indicators, load_history
from tradeforge.models import Order, OrderType
from tradeforge.simulator import Simulator

st.set_page_config(page_title="TradeForge", page_icon="📈", layout="wide")
st.title("TradeForge")
st.caption("Educational paper-trading simulator — simulated execution only")

if "sim" not in st.session_state:
    st.session_state.sim = Simulator()

sim = st.session_state.sim

with st.sidebar:
    st.header("Market")
    symbol = st.text_input("Symbol", "AAPL").upper()
    period = st.selectbox("History", ["5d", "1mo", "3mo"], index=1)
    interval = st.selectbox("Interval", ["5m", "15m", "1h", "1d"], index=0)
    if st.button("Load market data"):
        try:
            st.session_state.market = add_indicators(load_history(symbol, period, interval))
            st.success(f"Loaded {symbol}")
        except Exception as exc:
            st.error(str(exc))
    if st.button("Reset account"):
        sim.reset()
        st.rerun()

market = st.session_state.get("market")
if market is None:
    st.info("Load historical market data from the sidebar to begin a simulation.")
    st.stop()

latest = market.iloc[-1]
price = float(latest["close"])

m1, m2, m3, m4 = st.columns(4)
prices = {s: price for s in sim.account.positions}
m1.metric("Equity", f"${sim.account.equity(prices):,.2f}")
m2.metric("Cash", f"${sim.account.cash:,.2f}")
m3.metric("Realized P&L", f"${sim.account.realized_pnl:,.2f}")
m4.metric("Commissions", f"${sim.account.commissions:,.2f}")

fig = go.Figure(go.Candlestick(x=market.index, open=market.open, high=market.high, low=market.low, close=market.close, name=symbol))
fig.add_trace(go.Scatter(x=market.index, y=market.sma_20, name="SMA 20"))
fig.add_trace(go.Scatter(x=market.index, y=market.ema_20, name="EMA 20"))
fig.add_trace(go.Scatter(x=market.index, y=market.vwap, name="VWAP"))
fig.update_layout(height=520, xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Order Ticket")
c1, c2, c3, c4 = st.columns(4)
side = c1.selectbox("Side", ["buy", "sell"])
qty = c2.number_input("Quantity", min_value=1, value=10, step=1)
order_type = c3.selectbox("Order type", [x.value for x in OrderType])
limit_price = c4.number_input("Limit price", min_value=0.0, value=price, step=0.01) if order_type == "limit" else None

if st.button("Submit simulated order"):
    order = Order(symbol=symbol, side=side, quantity=int(qty), order_type=OrderType(order_type), limit_price=limit_price)
    sim.submit(order, price)
    st.success(f"Order status: {order.status.value}")

st.subheader("Open Positions")
rows = []
for p in sim.account.positions.values():
    rows.append({"Symbol": p.symbol, "Shares": p.quantity, "Avg Cost": p.average_cost, "Market Value": p.market_value(price), "Unrealized P&L": p.unrealized_pnl(price)})
st.dataframe(rows, use_container_width=True)

st.subheader("Order Blotter")
st.dataframe([{"Symbol": o.symbol, "Side": o.side, "Qty": o.quantity, "Type": o.order_type.value, "Status": o.status.value, "Fill Qty": o.filled_quantity, "Avg Fill": o.average_fill_price, "Reason": o.reason} for o in sim.orders], use_container_width=True)
