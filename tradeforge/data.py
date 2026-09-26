import pandas as pd
import yfinance as yf


def load_history(symbol: str, period: str = "1mo", interval: str = "5m") -> pd.DataFrame:
    df = yf.download(symbol, period=period, interval=interval, auto_adjust=False, progress=False)
    if df.empty:
        raise ValueError(f"No market data returned for {symbol}")
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=str.lower)
    return df.dropna(subset=["close"])


def add_indicators(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["sma_20"] = out["close"].rolling(20).mean()
    out["ema_20"] = out["close"].ewm(span=20, adjust=False).mean()
    typical = (out["high"] + out["low"] + out["close"]) / 3
    out["vwap"] = (typical * out["volume"]).cumsum() / out["volume"].cumsum().replace(0, pd.NA)
    delta = out["close"].diff()
    gain = delta.clip(lower=0).rolling(14).mean()
    loss = (-delta.clip(upper=0)).rolling(14).mean()
    rs = gain / loss.replace(0, pd.NA)
    out["rsi"] = 100 - (100 / (1 + rs))
    return out
