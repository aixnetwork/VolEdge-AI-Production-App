from __future__ import annotations

from statistics import mean

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
    relative_volume = latest.volume / max(1, avg_volume)
    ema_10 = _ema(bars, 10)
    ema_21 = _ema(bars, 21)
    ema_50 = _ema(bars, 50)
    bullish_trend_score = 96 if latest.close > ema_10 > ema_21 > ema_50 else 78 if latest.close > ema_21 > ema_50 else 55 if latest.close > ema_50 else 38
    bearish_trend_score = 96 if latest.close < ema_10 < ema_21 < ema_50 else 78 if latest.close < ema_21 < ema_50 else 55 if latest.close < ema_50 else 38
    rising_lows = bars[-1].low > bars[-5].low > bars[-12].low
    falling_highs = bars[-1].high < bars[-5].high < bars[-12].high
    bullish_pressure = latest.close >= (range_low + (range_high - range_low) * 0.62)
    bearish_pressure = latest.close <= (range_low + (range_high - range_low) * 0.38)
    evidence: list[str] = []

    if breakout_strength > 0.4 and volume_surge > 8:
        name = "Gap Breakout" if latest.open > range_high else "Breakout"
        direction = "Bullish"
        raw_quality = 68 + breakout_strength * 5 + min(volume_surge, 40) * 0.35
        evidence = ["price closed above resistance", f"relative volume {relative_volume:.2f}x", "breakout already confirmed"]
    elif breakdown_strength > 0.4 and volume_surge > 8:
        name = "Breakdown"
        direction = "Bearish"
        raw_quality = 64 + breakdown_strength * 5 + min(volume_surge, 40) * 0.35
        evidence = ["price closed below support", f"relative volume {relative_volume:.2f}x", "breakdown already confirmed"]
    elif 0 <= distance_to_high <= 1.8 and compression >= 8 and rising_lows and bullish_pressure:
        name = "Pre-Breakout Compression"
        direction = "Bullish"
        raw_quality = 72 + min(compression, 35) * 0.45 + min(volume_dryup, 35) * 0.22 + max(0, 4 - range_width) * 1.8
        evidence = ["tight range compression", "rising lows", f"{distance_to_high:.2f}% below resistance"]
    elif 0 <= distance_to_low <= 1.8 and compression >= 8 and falling_highs and bearish_pressure:
        name = "Pre-Breakdown Distribution"
        direction = "Bearish"
        raw_quality = 70 + min(compression, 35) * 0.45 + min(volume_dryup, 35) * 0.18 + max(0, 4 - range_width) * 1.8
        evidence = ["tight range compression", "falling highs", f"{distance_to_low:.2f}% above support"]
    elif bars[-1].close > bars[-8].close > bars[-21].close:
        name = "Bull Flag"
        direction = "Bullish"
        raw_quality = 88
        evidence = ["multi-week momentum stair-step", "price holding above short-term trend", f"relative volume {relative_volume:.2f}x"]
    elif bars[-1].close < bars[-8].close < bars[-21].close:
        name = "Bear Flag"
        direction = "Bearish"
        raw_quality = 84
        evidence = ["multi-week downside stair-step", "price below short-term trend", f"relative volume {relative_volume:.2f}x"]
    else:
        name = "Volatility Expansion"
        direction = "Neutral"
        raw_quality = 61
        evidence = ["range expansion without clean direction", f"ATR compression {compression:.1f}", f"relative volume {relative_volume:.2f}x"]

    quality = min(100, raw_quality)
    trend_score = bearish_trend_score if direction == "Bearish" else bullish_trend_score if direction == "Bullish" else 58
    level_score = max(0, 100 - min(100, min(abs(distance_to_high), abs(distance_to_low)) * 30))
    volume_score = min(100, 62 + (relative_volume - 1) * 60) if not name.startswith("Pre-") else min(100, 76 + volume_dryup * 0.35)
    timing_score = 94 if name.startswith("Pre-") else 82 if name in {"Breakout", "Gap Breakout", "Breakdown"} else 70
    chart_score = min(100, quality * 0.38 + trend_score * 0.24 + volume_score * 0.16 + timing_score * 0.14 + level_score * 0.08)
    if direction == "Bullish":
        breakout_probability = min(100, max(0, chart_score * 0.86 + historical_accuracy * 0.14))
        breakdown_probability = max(0, 100 - breakout_probability - 8)
        predicted_move = "Buy trigger forming" if name.startswith("Pre-") else "Bullish follow-through"
        key_level = range_high
    elif direction == "Bearish":
        breakdown_probability = min(100, max(0, chart_score * 0.86 + historical_accuracy * 0.14))
        breakout_probability = max(0, 100 - breakdown_probability - 8)
        predicted_move = "Sell trigger forming" if name.startswith("Pre-") else "Bearish follow-through"
        key_level = range_low
    else:
        breakout_probability = breakdown_probability = min(54, chart_score * 0.62)
        predicted_move = "Wait for range break"
        key_level = range_high if latest.close >= (range_high + range_low) / 2 else range_low

    analog = _historical_pattern_analogs(bars)
    analog_count = int(analog["count"])
    analog_bias = str(analog["bias"])
    analog_confidence = float(analog["confidence"])
    analog_win_rate = float(analog["win_rate"])
    analog_average_return = float(analog["average_return"])
    if analog_count >= 8 and analog_bias != "Neutral":
        evidence.append(
            f"historical analogs lean {analog_bias.lower()} in {analog_win_rate:.0f}% of {analog_count} similar setups"
        )
        evidence.append(f"5-day analog average return {analog_average_return:+.2f}%")
        if direction == "Neutral" and analog_confidence >= 55:
            direction = analog_bias  # type: ignore[assignment]
            name = f"Historical {analog_bias} Analog"
            chart_score = max(chart_score, min(82, analog_confidence * 0.9 + quality * 0.1))
            predicted_move = "Buy trigger forming" if direction == "Bullish" else "Sell trigger forming"
            key_level = range_high if direction == "Bullish" else range_low
        elif direction != analog_bias and analog_confidence >= 68:
            chart_score = max(48, chart_score - min(14, (analog_confidence - 55) * 0.45))
            predicted_move = "Wait - historical analog conflict"
            evidence.append("current chart signal conflicts with stronger historical analogs")

        analog_side_score = min(100, analog_confidence * 0.78 + analog_win_rate * 0.22)
        if analog_bias == "Bullish":
            breakout_probability = min(100, breakout_probability * 0.62 + analog_side_score * 0.38)
            breakdown_probability = max(0, breakdown_probability * 0.72 + max(0, 100 - analog_side_score - 8) * 0.28)
        elif analog_bias == "Bearish":
            breakdown_probability = min(100, breakdown_probability * 0.62 + analog_side_score * 0.38)
            breakout_probability = max(0, breakout_probability * 0.72 + max(0, 100 - analog_side_score - 8) * 0.28)

    prediction_score = chart_score
    if analog_count >= 8:
        prediction_score = min(100, chart_score * 0.7 + analog_confidence * 0.3)
    chart_summary = _chart_summary(name, direction, chart_score, key_level)
    confidence = "High" if quality >= 80 and historical_accuracy >= 55 else "Medium" if quality >= 65 else "Low"
    return PatternSignal(
        name=name,
        quality_score=round(quality, 2),
        historical_accuracy=historical_accuracy,
        confidence_level=confidence,
        direction=direction,
        chart_score=round(chart_score, 2),
        prediction_score=round(prediction_score, 2),
        breakout_probability=round(breakout_probability, 2),
        breakdown_probability=round(breakdown_probability, 2),
        predicted_move=predicted_move,
        key_level=round(key_level, 2),
        chart_summary=chart_summary,
        evidence=evidence,
        analog_count=analog_count,
        analog_win_rate=round(analog_win_rate, 2),
        analog_average_return=round(analog_average_return, 2),
        analog_bias=analog_bias,
        analog_confidence=round(analog_confidence, 2),
    )


def _ema(bars: list[OhlcvBar], period: int) -> float:
    values = [bar.close for bar in bars[-period:]]
    if not values:
        return bars[-1].close
    alpha = 2 / (len(values) + 1)
    ema = values[0]
    for value in values[1:]:
        ema = value * alpha + ema * (1 - alpha)
    return ema


def _chart_summary(name: str, direction: str, chart_score: float, key_level: float) -> str:
    if direction == "Bullish":
        return f"{name} has a {chart_score:.0f}/100 AI chart score with resistance near {key_level:.2f}."
    if direction == "Bearish":
        return f"{name} has a {chart_score:.0f}/100 AI chart score with support near {key_level:.2f}."
    return f"{name} is active, but the AI chart model is waiting for a clean break near {key_level:.2f}."


def _historical_pattern_analogs(bars: list[OhlcvBar], holding_period: int = 5) -> dict[str, float | int | str]:
    if len(bars) < 90:
        return _empty_analog_result()

    current = _feature_snapshot(bars, len(bars) - 1)
    analogs: list[tuple[float, float]] = []
    end = len(bars) - holding_period - 8
    for index in range(55, max(55, end)):
        past = _feature_snapshot(bars, index)
        similarity = _feature_similarity(current, past)
        if similarity < 60:
            continue
        forward_return = (bars[index + holding_period].close - bars[index].close) / bars[index].close * 100
        analogs.append((similarity, forward_return))

    if not analogs:
        return _empty_analog_result()

    top_analogs = sorted(analogs, key=lambda item: item[0], reverse=True)[:32]
    returns = [item[1] for item in top_analogs]
    bullish = sum(1 for value in returns if value > 0.2)
    bearish = sum(1 for value in returns if value < -0.2)
    average_return = mean(returns)
    count = len(top_analogs)
    if bullish > bearish and average_return > 0:
        bias = "Bullish"
        directional_hits = bullish
    elif bearish > bullish and average_return < 0:
        bias = "Bearish"
        directional_hits = bearish
    else:
        bias = "Neutral"
        directional_hits = max(bullish, bearish)

    win_rate = directional_hits / count * 100
    average_similarity = mean(item[0] for item in top_analogs)
    edge = abs(bullish - bearish) / count * 100
    confidence = win_rate * 0.46 + average_similarity * 0.28 + edge * 0.16 + min(10, abs(average_return) * 3.5)
    if count < 16:
        confidence *= 0.88

    return {
        "count": count,
        "win_rate": min(100, max(0, win_rate)),
        "average_return": average_return,
        "bias": bias,
        "confidence": min(100, max(0, confidence)),
    }


def _empty_analog_result() -> dict[str, float | int | str]:
    return {
        "count": 0,
        "win_rate": 0,
        "average_return": 0,
        "bias": "Neutral",
        "confidence": 0,
    }


def _feature_snapshot(bars: list[OhlcvBar], index: int) -> dict[str, float]:
    close = bars[index].close
    window = bars[: index + 1]
    ema_10 = _ema(window, 10)
    ema_21 = _ema(window, 21)
    ema_50 = _ema(window, 50)
    range_bars = bars[max(0, index - 15) : index] or bars[max(0, index - 16) : index + 1]
    range_high = max(bar.high for bar in range_bars)
    range_low = min(bar.low for bar in range_bars)
    recent_ranges = [bar.high - bar.low for bar in bars[max(0, index - 7) : index + 1]]
    prior_ranges = [bar.high - bar.low for bar in bars[max(0, index - 35) : max(1, index - 15)]]
    recent_atr = mean(recent_ranges)
    prior_atr = mean(prior_ranges) if prior_ranges else recent_atr
    avg_volume = mean(bar.volume for bar in bars[max(0, index - 20) : index] or [bars[index]])
    bar_range = max(0.01, bars[index].high - bars[index].low)
    range_span = max(0.01, range_high - range_low)
    return {
        "trend_10_50": (ema_10 - ema_50) / max(0.01, close) * 100,
        "trend_21_50": (ema_21 - ema_50) / max(0.01, close) * 100,
        "momentum_5": (close - bars[index - 5].close) / max(0.01, bars[index - 5].close) * 100,
        "momentum_21": (close - bars[index - 21].close) / max(0.01, bars[index - 21].close) * 100,
        "range_position": (close - range_low) / range_span,
        "range_width": range_span / max(0.01, close) * 100,
        "relative_volume": bars[index].volume / max(1, avg_volume),
        "atr_ratio": recent_atr / max(0.01, prior_atr),
        "candle_pressure": (close - bars[index].open) / bar_range,
    }


def _feature_similarity(current: dict[str, float], past: dict[str, float]) -> float:
    scales = {
        "trend_10_50": 5.0,
        "trend_21_50": 5.0,
        "momentum_5": 5.0,
        "momentum_21": 9.0,
        "range_position": 0.35,
        "range_width": 8.0,
        "relative_volume": 1.35,
        "atr_ratio": 0.85,
        "candle_pressure": 0.85,
    }
    weights = {
        "trend_10_50": 0.14,
        "trend_21_50": 0.12,
        "momentum_5": 0.13,
        "momentum_21": 0.14,
        "range_position": 0.16,
        "range_width": 0.1,
        "relative_volume": 0.09,
        "atr_ratio": 0.07,
        "candle_pressure": 0.05,
    }
    distance = 0.0
    for key, scale in scales.items():
        distance += min(2.4, abs(current[key] - past[key]) / scale) * weights[key]
    return max(0, 100 - distance * 30)
