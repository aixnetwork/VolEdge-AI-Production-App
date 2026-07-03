from __future__ import annotations

from .engines.accuracy import calculate_historical_accuracy
from .engines.patterns import detect_primary_pattern
from .engines.voledge_score import score_opportunity
from .market_data import ETF_UNIVERSE
from .models import Intelligence, Recommendation
from .providers import get_market_data_provider


RADAR_PRIORITY_SYMBOLS = [
    "SPY",
    "QQQ",
    "IWM",
    "XLK",
    "SOXX",
    "SOXL",
    "SOXS",
    "UVIX",
    "VIXY",
    "SVIX",
    "GLD",
    "SLV",
    "GDX",
    "XLF",
    "XLE",
    "XBI",
    "LABU",
    "LABD",
    "IBIT",
    "FBTC",
    "BITB",
    "ARKB",
    "BITO",
    "BITU",
    "SBIT",
    "ETHA",
    "FETH",
    "ETHW",
]


def build_intelligence(symbol: str) -> Intelligence:
    bars = get_market_data_provider().history(symbol)
    baseline_accuracy = calculate_historical_accuracy(bars, quality_threshold=0.012)
    pattern = detect_primary_pattern(bars, baseline_accuracy.historical_accuracy)
    accuracy = calculate_historical_accuracy(bars, quality_threshold=0.012, direction=pattern.direction)
    pattern = detect_primary_pattern(bars, accuracy.historical_accuracy)
    latest = bars[-1]
    atr = sum(bar.high - bar.low for bar in bars[-14:]) / 14
    resistance = max(bar.high for bar in bars[-16:-1])
    support = min(bar.low for bar in bars[-16:-1])
    avg_volume = sum(bar.volume for bar in bars[-21:-1]) / 20
    volume_ratio = latest.volume / max(1, avg_volume)
    short_average = sum(bar.close for bar in bars[-10:]) / 10
    long_average = sum(bar.close for bar in bars[-30:]) / 30
    if pattern.direction == "Bearish":
        entry = min(latest.close, support - atr * 0.08) if pattern.name.startswith("Pre-Breakdown") else latest.close
        stop = max(resistance, entry + atr * 1.05)
        target = entry - atr * 2.0
    else:
        entry = max(latest.close, resistance + atr * 0.08) if pattern.name.startswith("Pre-Breakout") else latest.close
        stop = min(support, entry - atr * 1.05)
        target = entry + atr * 2.2
    score = score_opportunity(bars, accuracy, pattern, entry, stop, target)
    if pattern.direction == "Bearish":
        recommendation = Recommendation.STRONG_SELL if score >= 73 else Recommendation.HEDGE if score >= 62 else Recommendation.WATCH
    elif pattern.direction == "Neutral":
        recommendation = Recommendation.WATCH
    else:
        recommendation = Recommendation.EXTREME_BUY if score >= 85 else Recommendation.STRONG_BUY if score >= 73 else Recommendation.WATCH
    confidence_level = "Very High" if score >= 88 and accuracy.historical_accuracy >= 65 else pattern.confidence_level
    risk_reward = abs(target - entry) / max(0.01, abs(entry - stop))
    category = ETF_UNIVERSE[symbol][0]
    trigger_label = (
        "sell trigger below support"
        if pattern.direction == "Bearish"
        else "buy trigger above resistance"
        if pattern.direction == "Bullish"
        else "watch trigger near the current range"
    )
    setup_stage = "early setup" if pattern.name.startswith("Pre-") else "confirmed move"
    trend_label = (
        "trend-aligned"
        if (pattern.direction == "Bearish" and latest.close < short_average < long_average)
        or (pattern.direction != "Bearish" and latest.close > short_average > long_average)
        else "mixed-trend"
    )
    volume_label = "rising volume" if volume_ratio >= 1.12 else "normal volume" if volume_ratio >= 0.85 else "light volume"
    explanation = (
        f"{symbol} is a {setup_stage} with a {trigger_label} near {entry:.2f}. "
        f"Its {pattern.name.lower()} has a "
        f"{pattern.quality_score:.0f}/100 pattern quality score, {accuracy.historical_accuracy:.0f}% "
        f"directional historical accuracy across {accuracy.matching_setups} matching setups, and a calculated "
        f"{accuracy.expected_return:.2f}% expected return over the best window. "
        f"The swing-trade filter reads {trend_label} with {volume_label} at {volume_ratio:.2f}x the recent average."
    )
    return Intelligence(
        symbol=symbol,
        category=category,
        vol_edge_score=score,
        historical_accuracy=accuracy.historical_accuracy,
        confidence_level=confidence_level,
        historical_matches=accuracy.matching_setups,
        expected_return=accuracy.expected_return,
        best_holding_window=accuracy.best_holding_window,
        recommendation=recommendation,
        pattern=pattern,
        suggested_entry=round(entry, 2),
        suggested_stop_loss=round(stop, 2),
        suggested_target=round(target, 2),
        risk_reward=round(risk_reward, 2),
        ai_explanation=explanation,
    )


def opportunity_radar() -> list[Intelligence]:
    opportunities = []
    for symbol in RADAR_PRIORITY_SYMBOLS:
        if symbol not in ETF_UNIVERSE:
            continue
        try:
            opportunities.append(build_intelligence(symbol))
        except Exception:
            continue
    if not opportunities:
        opportunities = [build_intelligence(symbol) for symbol in ("SPY", "QQQ", "GLD")]
    return sorted(opportunities, key=lambda item: item.vol_edge_score, reverse=True)
