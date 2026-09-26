import math
import numpy as np
import pandas as pd


def performance_metrics(equity: pd.Series) -> dict[str, float]:
    equity = equity.dropna().astype(float)
    if len(equity) < 2:
        return {"total_return": 0.0, "volatility": 0.0, "sharpe": 0.0, "max_drawdown": 0.0}
    returns = equity.pct_change().dropna()
    total_return = equity.iloc[-1] / equity.iloc[0] - 1
    volatility = returns.std(ddof=1) * math.sqrt(252)
    sharpe = (returns.mean() / returns.std(ddof=1)) * math.sqrt(252) if returns.std(ddof=1) else 0.0
    drawdown = equity / equity.cummax() - 1
    return {
        "total_return": float(total_return),
        "volatility": float(volatility),
        "sharpe": float(sharpe),
        "max_drawdown": float(drawdown.min()),
    }
