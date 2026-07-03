from __future__ import annotations

from ..models import OhlcvBar, PatternSignal


def detect_primary_pattern(bars: list[OhlcvBar], historical_accuracy: float) -> PatternSignal:
    latest = bars[-1]
    prior = bars[-16:-1]
    range_high = max(bar.high for bar in prior)
    range_low = min(bar.low for bar in prior)
    avg_volume = sum(bar.volume for bar in prior) / len(prior)
    breakout_strength = max(0, (latest.close - range_high) / latest.close * 100)
    breakdown_strength = max(0, (range_low - latest.close) / latest.close * 100)
    volume_surge = max(0, (latest.volume / avg_volume - 1) * 100)

    if breakout_strength > 0.4 and volume_surge > 8:
        name = "Gap Breakout" if latest.open > range_high else "Breakout"
        direction = "Bullish"
        raw_quality = 68 + breakout_strength * 5 + min(volume_surge, 40) * 0.35
    elif breakdown_strength > 0.4 and volume_surge > 8:
        name = "Breakdown"
        direction = "Bearish"
        raw_quality = 64 + breakdown_strength * 5 + min(volume_surge, 40) * 0.35
    elif bars[-1].close > bars[-8].close > bars[-21].close:
        name = "Bull Flag"
        direction = "Bullish"
        raw_quality = 88
    elif bars[-1].close < bars[-8].close < bars[-21].close:
        name = "Bear Flag"
        direction = "Bearish"
        raw_quality = 84
    else:
        name = "Volatility Expansion"
        direction = "Neutral"
        raw_quality = 61

    quality = min(100, raw_quality)
    confidence = "High" if quality >= 80 and historical_accuracy >= 55 else "Medium" if quality >= 65 else "Low"
    return PatternSignal(
        name=name,
        quality_score=round(quality, 2),
        historical_accuracy=historical_accuracy,
        confidence_level=confidence,
        direction=direction,
    )
