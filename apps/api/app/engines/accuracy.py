from __future__ import annotations

from statistics import mean

from ..market_data import returns
from ..models import AccuracyStats, OhlcvBar


def calculate_historical_accuracy(
    bars: list[OhlcvBar],
    quality_threshold: float = 0.0,
    direction: str = "Bullish",
) -> AccuracyStats:
    period_returns = returns(bars, holding_period=5)
    matching = [value for value in period_returns if abs(value) >= quality_threshold]
    wants_downside = direction == "Bearish"
    wins = [value for value in matching if value < 0] if wants_downside else [value for value in matching if value > 0]
    losses = [value for value in matching if value >= 0] if wants_downside else [value for value in matching if value <= 0]

    matching_setups = len(matching)
    win_rate = len(wins) / matching_setups * 100 if matching_setups else 0
    directional_returns = [-value for value in matching] if wants_downside else matching
    directional_wins = [-value for value in wins] if wants_downside else wins
    directional_losses = [-value for value in losses] if wants_downside else losses
    average_return = mean(directional_returns) * 100 if directional_returns else 0
    average_drawdown = mean(directional_losses) * 100 if directional_losses else 0
    gross_profit = sum(directional_wins)
    gross_loss = abs(sum(directional_losses))
    profit_factor = gross_profit / gross_loss if gross_loss else gross_profit or 1
    confidence = "High" if matching_setups >= 70 and win_rate >= 55 else "Medium" if matching_setups >= 35 else "Low"

    return AccuracyStats(
        historical_win_rate=round(win_rate, 2),
        historical_accuracy=round(win_rate, 2),
        matching_setups=matching_setups,
        average_return=round(average_return, 2),
        average_drawdown=round(average_drawdown, 2),
        profit_factor=round(profit_factor, 2),
        expected_return=round(average_return * (win_rate / 100), 2),
        best_holding_window="5 trading days",
        confidence_level=confidence,
    )
