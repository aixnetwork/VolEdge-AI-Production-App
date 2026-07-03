from __future__ import annotations

from ..models import AccuracyStats, InstitutionalConfirmation, MarketRegime, MultiTimeframeConfirmation, OhlcvBar, PatternSignal


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
    market_regime: MarketRegime | None = None,
    timeframe: MultiTimeframeConfirmation | None = None,
    institutional: InstitutionalConfirmation | None = None,
    adaptive_weights: dict[str, float] | None = None,
) -> float:
    factors = _factor_scores(bars, accuracy, pattern, entry, stop, target, timeframe, institutional)
    weights = adaptive_weights or adaptive_factor_weights(bars, pattern.direction)
    score = sum(factors[name] * weights.get(name, 0) for name in factors)
    if market_regime:
        score += _regime_adjustment(market_regime, pattern.direction)
    return round(min(100, max(0, score)), 2)


def adaptive_factor_weights(bars: list[OhlcvBar], direction: str) -> dict[str, float]:
    base = {
        "accuracy": 0.22,
        "pattern": 0.16,
        "volatility": 0.12,
        "momentum": 0.12,
        "risk_reward": 0.10,
        "volume": 0.10,
        "trend": 0.10,
        "timeframe": 0.04,
        "institutional": 0.04,
    }
    performance = {
        "momentum": _recent_factor_hit_rate(bars, "momentum", direction),
        "trend": _recent_factor_hit_rate(bars, "trend", direction),
        "volume": _recent_factor_hit_rate(bars, "volume", direction),
        "volatility": _recent_factor_hit_rate(bars, "volatility", direction),
    }
    raw = dict(base)
    for factor, hit_rate in performance.items():
        raw[factor] *= 0.70 + hit_rate / 100 * 0.70
    total = sum(raw.values())
    return {name: round(value / total, 4) for name, value in raw.items()}


def _factor_scores(
    bars: list[OhlcvBar],
    accuracy: AccuracyStats,
    pattern: PatternSignal,
    entry: float,
    stop: float,
    target: float,
    timeframe: MultiTimeframeConfirmation | None,
    institutional: InstitutionalConfirmation | None,
) -> dict[str, float]:
    return {
        "accuracy": accuracy.historical_accuracy,
        "pattern": pattern.quality_score,
        "volatility": _atr_score(bars),
        "momentum": _momentum_score(bars, pattern.direction),
        "risk_reward": _risk_reward_score(entry, stop, target),
        "volume": _volume_confirmation_score(bars, pattern),
        "trend": _trend_alignment_score(bars, pattern.direction),
        "timeframe": timeframe.alignment_score if timeframe else 58,
        "institutional": institutional.confirmation_score if institutional else 58,
    }


def _recent_factor_hit_rate(bars: list[OhlcvBar], factor: str, direction: str) -> float:
    wants_downside = direction == "Bearish"
    hits = 0
    total = 0
    for index in range(max(42, len(bars) - 126), len(bars) - 5):
        if not _factor_was_active(bars, index, factor, wants_downside):
            continue
        forward = (bars[index + 5].close - bars[index].close) / bars[index].close
        won = forward < 0 if wants_downside else forward > 0
        hits += 1 if won else 0
        total += 1
    return hits / total * 100 if total else 52.5


def _factor_was_active(bars: list[OhlcvBar], index: int, factor: str, wants_downside: bool) -> bool:
    close = bars[index].close
    short = sum(bar.close for bar in bars[index - 9 : index + 1]) / 10
    long = sum(bar.close for bar in bars[index - 29 : index + 1]) / 30
    volume = bars[index].volume / max(1, sum(bar.volume for bar in bars[index - 20 : index]) / 20)
    recent_atr = sum(bar.high - bar.low for bar in bars[index - 13 : index + 1]) / 14
    prior_atr = sum(bar.high - bar.low for bar in bars[index - 41 : index - 13]) / 28
    if factor == "momentum":
        return close < bars[index - 10].close if wants_downside else close > bars[index - 10].close
    if factor == "trend":
        return close < short < long if wants_downside else close > short > long
    if factor == "volume":
        return volume >= 1.05
    if factor == "volatility":
        return recent_atr >= prior_atr * 0.95
    return False


def _regime_adjustment(market_regime: MarketRegime, direction: str) -> float:
    if market_regime.name in {"Bull Market", "Risk-On"} and direction == "Bullish":
        return 3
    if market_regime.name in {"Bear Market", "Risk-Off", "Crisis Mode"} and direction == "Bearish":
        return 3
    if market_regime.name == "Crisis Mode" and direction == "Bullish":
        return -7
    return market_regime.confidence_modifier * 0.35
