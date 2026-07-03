from __future__ import annotations

from ..models import AccuracyStats, OhlcvBar, PatternSignal


def _atr_score(bars: list[OhlcvBar]) -> float:
    recent = bars[-14:]
    prior = bars[-42:-14]
    recent_atr = sum(bar.high - bar.low for bar in recent) / len(recent)
    prior_atr = sum(bar.high - bar.low for bar in prior) / len(prior)
    return min(100, max(0, recent_atr / prior_atr * 84))


def _momentum_score(bars: list[OhlcvBar]) -> float:
    short = bars[-1].close - bars[-10].close
    long = bars[-1].close - bars[-30].close
    return min(100, max(0, 58 + short * 2.6 + long * 1.25))


def _risk_reward_score(entry: float, stop: float, target: float) -> float:
    risk = max(0.01, entry - stop)
    reward = max(0.01, target - entry)
    return min(100, reward / risk * 52)


def score_opportunity(
    bars: list[OhlcvBar],
    accuracy: AccuracyStats,
    pattern: PatternSignal,
    entry: float,
    stop: float,
    target: float,
) -> float:
    volatility = _atr_score(bars)
    momentum = _momentum_score(bars)
    risk_reward = _risk_reward_score(entry, stop, target)
    score = (
        accuracy.historical_accuracy * 0.30
        + pattern.quality_score * 0.25
        + volatility * 0.20
        + momentum * 0.15
        + risk_reward * 0.10
    )
    return round(min(100, max(0, score)), 2)
