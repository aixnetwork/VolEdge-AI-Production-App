from __future__ import annotations

from statistics import mean

from ..market_data import returns
from ..models import AccuracyStats, OhlcvBar


def calculate_historical_accuracy(
    bars: list[OhlcvBar],
    quality_threshold: float = 0.0,
    direction: str = "Bullish",
) -> AccuracyStats:
    candidates = [
        _score_holding_window(bars, quality_threshold, direction, holding_period)
        for holding_period in (3, 5, 8)
    ]
    best = max(candidates, key=lambda item: (item["historical_accuracy"], item["expected_return"], item["matching_setups"]))

    return AccuracyStats(
        historical_win_rate=best["historical_win_rate"],
        historical_accuracy=best["historical_accuracy"],
        matching_setups=best["matching_setups"],
        average_return=best["average_return"],
        average_drawdown=best["average_drawdown"],
        profit_factor=best["profit_factor"],
        expected_return=best["expected_return"],
        best_holding_window=f"{best['holding_period']} trading days",
        confidence_level=best["confidence_level"],
    )


def _score_holding_window(
    bars: list[OhlcvBar],
    quality_threshold: float,
    direction: str,
    holding_period: int,
) -> dict[str, float | int | str]:
    matching = _matching_setup_returns(bars, quality_threshold, direction, holding_period)
    if len(matching) < 12:
        matching = [value for value in returns(bars, holding_period=holding_period) if abs(value) >= quality_threshold]

    wants_downside = direction == "Bearish"
    wins = [value for value in matching if value < 0] if wants_downside else [value for value in matching if value > 0]
    losses = [value for value in matching if value >= 0] if wants_downside else [value for value in matching if value <= 0]

    matching_setups = len(matching)
    win_rate = len(wins) / matching_setups * 100 if matching_setups else 0
    historical_accuracy = _confidence_adjusted_accuracy(len(wins), matching_setups)
    directional_returns = [-value for value in matching] if wants_downside else matching
    directional_wins = [-value for value in wins] if wants_downside else wins
    directional_losses = [-value for value in losses] if wants_downside else losses
    average_return = mean(directional_returns) * 100 if directional_returns else 0
    average_drawdown = mean(directional_losses) * 100 if directional_losses else 0
    gross_profit = sum(directional_wins)
    gross_loss = abs(sum(directional_losses))
    profit_factor = gross_profit / gross_loss if gross_loss else gross_profit or 1
    confidence = "High" if matching_setups >= 70 and win_rate >= 55 else "Medium" if matching_setups >= 35 else "Low"

    return {
        "historical_win_rate": round(win_rate, 2),
        "historical_accuracy": round(historical_accuracy, 2),
        "matching_setups": matching_setups,
        "average_return": round(average_return, 2),
        "average_drawdown": round(average_drawdown, 2),
        "profit_factor": round(profit_factor, 2),
        "expected_return": round(average_return * (win_rate / 100), 2),
        "holding_period": holding_period,
        "confidence_level": confidence,
    }


def _confidence_adjusted_accuracy(wins: int, total: int) -> float:
    if total <= 0:
        return 0
    market_prior = 52.5
    prior_weight = 18
    return (wins * 100 + market_prior * prior_weight) / (total + prior_weight)


def _matching_setup_returns(
    bars: list[OhlcvBar],
    quality_threshold: float,
    direction: str,
    holding_period: int,
) -> list[float]:
    wants_downside = direction == "Bearish"
    matches: list[float] = []
    for index in range(42, len(bars) - holding_period):
        close = bars[index].close
        short_average = mean(bar.close for bar in bars[index - 9 : index + 1])
        long_average = mean(bar.close for bar in bars[index - 29 : index + 1])
        recent_range = mean(bar.high - bar.low for bar in bars[index - 13 : index + 1])
        prior_range = mean(bar.high - bar.low for bar in bars[index - 41 : index - 13])
        range_expansion = recent_range >= prior_range * 0.92
        trend_aligned = close < short_average < long_average if wants_downside else close > short_average > long_average
        momentum_aligned = bars[index].close < bars[index - 10].close if wants_downside else bars[index].close > bars[index - 10].close

        if direction == "Neutral" or (trend_aligned and momentum_aligned and range_expansion):
            forward_return = (bars[index + holding_period].close - close) / close
            if abs(forward_return) >= quality_threshold:
                matches.append(forward_return)
    return matches
