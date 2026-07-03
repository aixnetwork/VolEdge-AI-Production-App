from __future__ import annotations

import math
from statistics import mean

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
    return score_setup_window(bars, quality_threshold, direction, holding_period)


def score_setup_window(
    bars: list[OhlcvBar],
    quality_threshold: float,
    direction: str,
    holding_period: int,
) -> dict[str, float | int | str]:
    matching = _matching_setup_returns(bars, quality_threshold, direction, holding_period, minimum_score=66)
    if len(matching) < 12:
        matching = _matching_setup_returns(bars, quality_threshold, direction, holding_period, minimum_score=58)
    if len(matching) < 8:
        matching = _best_scored_setup_returns(bars, quality_threshold, direction, holding_period, limit=18)

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
    profit_factor = gross_profit / gross_loss if gross_loss else 9.99 if wins else 1
    confidence = (
        "High"
        if (matching_setups >= 35 and win_rate >= 58) or (matching_setups >= 20 and win_rate >= 80)
        else "Medium"
        if (matching_setups >= 12 and win_rate >= 65) or matching_setups >= 28
        else "Low"
    )

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
    win_rate = wins / total
    z_score = 1.64
    denominator = 1 + z_score**2 / total
    center = win_rate + z_score**2 / (2 * total)
    margin = z_score * math.sqrt((win_rate * (1 - win_rate) + z_score**2 / (4 * total)) / total)
    lower_bound = (center - margin) / denominator
    if total >= 12:
        return lower_bound * 100
    sample_reliability = total / 12
    market_prior = 0.525
    return (lower_bound * sample_reliability + market_prior * (1 - sample_reliability)) * 100


def _matching_setup_returns(
    bars: list[OhlcvBar],
    quality_threshold: float,
    direction: str,
    holding_period: int,
    minimum_score: float,
) -> list[float]:
    return [
        forward_return
        for setup_score, forward_return in _scored_setup_returns(bars, quality_threshold, direction, holding_period)
        if setup_score >= minimum_score
    ]


def _best_scored_setup_returns(
    bars: list[OhlcvBar],
    quality_threshold: float,
    direction: str,
    holding_period: int,
    limit: int,
) -> list[float]:
    scored = _scored_setup_returns(bars, quality_threshold, direction, holding_period)
    return [forward_return for _, forward_return in sorted(scored, reverse=True)[:limit]]


def _scored_setup_returns(
    bars: list[OhlcvBar],
    quality_threshold: float,
    direction: str,
    holding_period: int,
) -> list[tuple[float, float]]:
    wants_downside = direction == "Bearish"
    matches: list[tuple[float, float]] = []
    for index in range(42, len(bars) - holding_period):
        close = bars[index].close
        short_average = mean(bar.close for bar in bars[index - 9 : index + 1])
        long_average = mean(bar.close for bar in bars[index - 29 : index + 1])
        recent_range = mean(bar.high - bar.low for bar in bars[index - 13 : index + 1])
        prior_range = mean(bar.high - bar.low for bar in bars[index - 41 : index - 13])
        avg_volume = mean(bar.volume for bar in bars[index - 20 : index])
        relative_volume = bars[index].volume / max(1, avg_volume)
        range_expansion = recent_range / max(0.01, prior_range)
        trend_aligned = close < short_average < long_average if wants_downside else close > short_average > long_average
        momentum_aligned = bars[index].close < bars[index - 10].close if wants_downside else bars[index].close > bars[index - 10].close
        near_range_edge = _range_edge_score(bars, index, wants_downside)
        setup_score = _setup_quality_score(
            trend_aligned=trend_aligned,
            momentum_aligned=momentum_aligned,
            range_expansion=range_expansion,
            relative_volume=relative_volume,
            near_range_edge=near_range_edge,
            neutral=direction == "Neutral",
        )

        if setup_score >= 45:
            forward_return = (bars[index + holding_period].close - close) / close
            if abs(forward_return) >= quality_threshold:
                matches.append((setup_score, forward_return))
    return matches


def _range_edge_score(bars: list[OhlcvBar], index: int, wants_downside: bool) -> float:
    range_high = max(bar.high for bar in bars[index - 15 : index])
    range_low = min(bar.low for bar in bars[index - 15 : index])
    close = bars[index].close
    if wants_downside:
        distance = max(0, (close - range_low) / close * 100)
    else:
        distance = max(0, (range_high - close) / close * 100)
    return max(0, 100 - min(100, distance * 28))


def _setup_quality_score(
    *,
    trend_aligned: bool,
    momentum_aligned: bool,
    range_expansion: float,
    relative_volume: float,
    near_range_edge: float,
    neutral: bool,
) -> float:
    if neutral:
        trend_score = 54
        momentum_score = 54
    else:
        trend_score = 100 if trend_aligned else 34
        momentum_score = 100 if momentum_aligned else 38
    range_score = max(0, min(100, 62 + (range_expansion - 0.9) * 95))
    volume_score = max(0, min(100, 58 + (relative_volume - 1) * 70))
    return (
        trend_score * 0.30
        + momentum_score * 0.24
        + range_score * 0.18
        + volume_score * 0.12
        + near_range_edge * 0.16
    )
