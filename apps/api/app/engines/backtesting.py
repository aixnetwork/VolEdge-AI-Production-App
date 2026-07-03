from __future__ import annotations

from statistics import mean

from ..market_data import returns
from ..models import BacktestResult, Intelligence
from ..providers import get_market_data_provider


def run_signal_backtest(intelligence: Intelligence) -> BacktestResult:
    bars = get_market_data_provider().history(intelligence.symbol)
    period_returns = returns(bars, holding_period=5)
    wins = [value for value in period_returns if value > 0]
    losses = [value for value in period_returns if value <= 0]
    gross_profit = sum(wins)
    gross_loss = abs(sum(losses))

    return BacktestResult(
        symbol=intelligence.symbol,
        strategy=f"{intelligence.pattern.name} with manual approval",
        trades=intelligence.historical_matches,
        win_rate=intelligence.historical_accuracy,
        expected_return=intelligence.expected_return,
        max_drawdown=round(abs(min(losses, default=0)) * 100, 2),
        profit_factor=round(gross_profit / gross_loss if gross_loss else gross_profit or 1, 2),
        best_window=intelligence.best_holding_window,
    )


def summarize_backtest_windows(symbol: str) -> list[dict[str, float | int | str]]:
    bars = get_market_data_provider().history(symbol)
    windows = []
    for holding_period in (3, 5, 8):
        period_returns = returns(bars, holding_period=holding_period)
        wins = [value for value in period_returns if value > 0]
        windows.append(
            {
                "window": f"{holding_period} trading days",
                "trades": len(period_returns),
                "win_rate": round(len(wins) / len(period_returns) * 100, 2),
                "average_return": round(mean(period_returns) * 100, 2),
                "max_drawdown": round(abs(min(period_returns, default=0)) * 100, 2),
            }
        )
    return windows
