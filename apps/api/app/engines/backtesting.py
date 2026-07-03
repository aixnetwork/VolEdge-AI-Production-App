from __future__ import annotations

from .accuracy import score_setup_window
from ..models import BacktestResult, Intelligence
from ..providers import get_market_data_provider


def run_signal_backtest(intelligence: Intelligence) -> BacktestResult:
    holding_period = _holding_period_from_label(intelligence.best_holding_window)
    metrics = _qualified_window_metrics(intelligence.symbol, intelligence.pattern.direction, holding_period)

    return BacktestResult(
        symbol=intelligence.symbol,
        strategy=f"{intelligence.pattern.name} qualified setup filter",
        trades=int(metrics["trades"]),
        win_rate=float(metrics["win_rate"]),
        expected_return=float(metrics["expected_return"]),
        max_drawdown=float(metrics["max_drawdown"]),
        profit_factor=float(metrics["profit_factor"]),
        best_window=intelligence.best_holding_window,
    )


def summarize_backtest_windows(symbol: str, direction: str = "Bullish") -> list[dict[str, float | int | str]]:
    return [_qualified_window_metrics(symbol, direction, holding_period) for holding_period in (3, 5, 8)]


def _qualified_window_metrics(symbol: str, direction: str, holding_period: int) -> dict[str, float | int | str]:
    bars = get_market_data_provider().history(symbol)
    metrics = score_setup_window(bars, quality_threshold=0.012, direction=direction, holding_period=holding_period)
    return {
        "window": f"{holding_period} trading days",
        "trades": metrics["matching_setups"],
        "win_rate": metrics["historical_accuracy"],
        "raw_win_rate": metrics["historical_win_rate"],
        "average_return": metrics["average_return"],
        "expected_return": metrics["expected_return"],
        "max_drawdown": abs(float(metrics["average_drawdown"])),
        "profit_factor": metrics["profit_factor"],
        "filter": "Qualified setup only",
    }


def _holding_period_from_label(label: str) -> int:
    for holding_period in (3, 5, 8):
        if label.startswith(str(holding_period)):
            return holding_period
    return 5
