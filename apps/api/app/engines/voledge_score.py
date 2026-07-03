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


def _volume_confirmation_score(bars: list[OhlcvBar], pattern: PatternSignal) -> float:
    recent_average = sum(bar.volume for bar in bars[-21:-1]) / 20
    current_ratio = bars[-1].volume / max(1, recent_average)
    if pattern.name.startswith("Pre-"):
        return min(100, max(35, 72 + (1.05 - current_ratio) * 45))
    return min(100, max(35, 52 + (current_ratio - 0.85) * 70))


def _trend_alignment_score(bars: list[OhlcvBar], direction: str) -> float:
    short_average = sum(bar.close for bar in bars[-10:]) / 10
    long_average = sum(bar.close for bar in bars[-30:]) / 30
    close = bars[-1].close
    if direction == "Bearish":
        if close < short_average < long_average:
            return 92
        if close < long_average:
            return 72
        return 44
    if direction == "Bullish":
        if close > short_average > long_average:
            return 92
        if close > long_average:
            return 72
        return 44
    return 58


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
    volume_confirmation = _volume_confirmation_score(bars, pattern)
    trend_alignment = _trend_alignment_score(bars, pattern.direction)
    setup_timing = _setup_timing_score(pattern)
    score = (
        accuracy.historical_accuracy * 0.24
        + pattern.quality_score * 0.20
        + volatility * 0.13
        + momentum * 0.11
        + risk_reward * 0.10
        + volume_confirmation * 0.08
        + trend_alignment * 0.06
        + setup_timing * 0.08
    )
    return round(min(100, max(0, score)), 2)
