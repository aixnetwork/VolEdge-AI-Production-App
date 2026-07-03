from __future__ import annotations

from ..models import AccuracyStats, OhlcvBar, PatternSignal


def _atr_score(bars: list[OhlcvBar]) -> float:
    recent = bars[-14:]
    prior = bars[-42:-14]
    recent_atr = sum(bar.high - bar.low for bar in recent) / len(recent)
    prior_atr = sum(bar.high - bar.low for bar in prior) / len(prior)
    return min(100, max(0, recent_atr / prior_atr * 84))


def _momentum_score(bars: list[OhlcvBar], direction: str) -> float:
    short = bars[-1].close - bars[-10].close
    long = bars[-1].close - bars[-30].close
    if direction == "Bearish":
        short = -short
        long = -long
    return min(100, max(0, 58 + short * 2.6 + long * 1.25))


def _risk_reward_score(entry: float, stop: float, target: float) -> float:
    risk = max(0.01, abs(entry - stop))
    reward = max(0.01, abs(target - entry))
    return min(100, reward / risk * 52)


def _setup_timing_score(pattern: PatternSignal) -> float:
    if pattern.name.startswith("Pre-Breakout") or pattern.name.startswith("Pre-Breakdown"):
        return 92
    if pattern.name in {"Breakout", "Gap Breakout", "Breakdown"}:
        return 76
    return 64


def score_opportunity(
    bars: list[OhlcvBar],
    accuracy: AccuracyStats,
    pattern: PatternSignal,
    entry: float,
    stop: float,
    target: float,
) -> float:
    volatility = _atr_score(bars)
    momentum = _momentum_score(bars, pattern.direction)
    risk_reward = _risk_reward_score(entry, stop, target)
    setup_timing = _setup_timing_score(pattern)
    score = (
        accuracy.historical_accuracy * 0.27
        + pattern.quality_score * 0.24
        + volatility * 0.17
        + momentum * 0.14
        + risk_reward * 0.10
        + setup_timing * 0.08
    )
    return round(min(100, max(0, score)), 2)
