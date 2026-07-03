from __future__ import annotations

from ..models import OhlcvBar, PatternSignal


def detect_primary_pattern(bars: list[OhlcvBar], historical_accuracy: float) -> PatternSignal:
    latest = bars[-1]
    prior = bars[-16:-1]
    recent = bars[-8:]
    baseline = bars[-36:-16]
    range_high = max(bar.high for bar in prior)
    range_low = min(bar.low for bar in prior)
    avg_volume = sum(bar.volume for bar in prior) / len(prior)
    recent_atr = sum(bar.high - bar.low for bar in recent) / len(recent)
    prior_atr = sum(bar.high - bar.low for bar in baseline) / len(baseline)
    range_width = max(0.01, (range_high - range_low) / latest.close * 100)
    breakout_strength = max(0, (latest.close - range_high) / latest.close * 100)
    breakdown_strength = max(0, (range_low - latest.close) / latest.close * 100)
    distance_to_high = (range_high - latest.close) / latest.close * 100
    distance_to_low = (latest.close - range_low) / latest.close * 100
    volume_surge = max(0, (latest.volume / avg_volume - 1) * 100)
    volume_dryup = max(0, (1 - latest.volume / avg_volume) * 100)
    compression = max(0, (1 - recent_atr / prior_atr) * 100) if prior_atr else 0
    rising_lows = bars[-1].low > bars[-5].low > bars[-12].low
    falling_highs = bars[-1].high < bars[-5].high < bars[-12].high
    bullish_pressure = latest.close >= (range_low + (range_high - range_low) * 0.62)
    bearish_pressure = latest.close <= (range_low + (range_high - range_low) * 0.38)

    if breakout_strength > 0.4 and volume_surge > 8:
        name = "Gap Breakout" if latest.open > range_high else "Breakout"
        direction = "Bullish"
        raw_quality = 68 + breakout_strength * 5 + min(volume_surge, 40) * 0.35
    elif breakdown_strength > 0.4 and volume_surge > 8:
        name = "Breakdown"
        direction = "Bearish"
        raw_quality = 64 + breakdown_strength * 5 + min(volume_surge, 40) * 0.35
    elif 0 <= distance_to_high <= 1.8 and compression >= 8 and rising_lows and bullish_pressure:
        name = "Pre-Breakout Compression"
        direction = "Bullish"
        raw_quality = 72 + min(compression, 35) * 0.45 + min(volume_dryup, 35) * 0.22 + max(0, 4 - range_width) * 1.8
    elif 0 <= distance_to_low <= 1.8 and compression >= 8 and falling_highs and bearish_pressure:
        name = "Pre-Breakdown Distribution"
        direction = "Bearish"
        raw_quality = 70 + min(compression, 35) * 0.45 + min(volume_dryup, 35) * 0.18 + max(0, 4 - range_width) * 1.8
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
