from __future__ import annotations

from .engines.accuracy import calculate_historical_accuracy
from .engines.confirmation import build_institutional_confirmation, build_timeframe_confirmation
from .engines.market_regime import classify_market_regime
from .engines.patterns import detect_primary_pattern
from .engines.voledge_score import adaptive_factor_weights, score_opportunity
from .market_data import ETF_UNIVERSE
from .models import EvidenceReport, Intelligence, Recommendation
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
    provider = get_market_data_provider()
    bars = provider.history(symbol)
    benchmark = provider.history("SPY") if symbol != "SPY" else bars
    qqq = provider.history("QQQ") if symbol != "QQQ" else bars
    try:
        volatility_proxy = provider.history("VIXY")
    except Exception:
        volatility_proxy = None
    market_regime = classify_market_regime(benchmark, qqq, volatility_proxy)
    baseline_accuracy = calculate_historical_accuracy(bars, quality_threshold=0.012)
    pattern = detect_primary_pattern(bars, baseline_accuracy.historical_accuracy)
    accuracy = calculate_historical_accuracy(bars, quality_threshold=0.012, direction=pattern.direction)
    pattern = detect_primary_pattern(bars, accuracy.historical_accuracy)
    timeframe = build_timeframe_confirmation(bars, pattern.direction)
    institutional = build_institutional_confirmation(bars, benchmark, pattern)
    latest = bars[-1]
    previous = bars[-2]
    try:
        quote = provider.quote(symbol)
    except Exception:
        change = latest.close - previous.close
        quote = None
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
    adaptive_weights = adaptive_factor_weights(bars, pattern.direction)
    score = score_opportunity(
        bars,
        accuracy,
        pattern,
        entry,
        stop,
        target,
        market_regime=market_regime,
        timeframe=timeframe,
        institutional=institutional,
        adaptive_weights=adaptive_weights,
    )
    confidence_score = _confidence_score(score, accuracy, pattern.quality_score, timeframe.alignment_score, institutional.confirmation_score, market_regime.confidence_modifier)
    risk_score = _risk_score(bars, accuracy.average_drawdown, risk_reward=abs(target - entry) / max(0.01, abs(entry - stop)), market_regime=market_regime.name)
    if pattern.direction == "Bearish":
        recommendation = Recommendation.STRONG_SELL if score >= 73 else Recommendation.HEDGE if score >= 62 else Recommendation.WATCH
    elif pattern.direction == "Neutral":
        recommendation = Recommendation.WATCH
    else:
        recommendation = Recommendation.EXTREME_BUY if score >= 85 else Recommendation.STRONG_BUY if score >= 73 else Recommendation.WATCH
    confidence_level = "Very High" if score >= 88 and accuracy.historical_accuracy >= 65 else pattern.confidence_level
    risk_reward = abs(target - entry) / max(0.01, abs(entry - stop))
    category = ETF_UNIVERSE[symbol][0]
    latest_price = quote.price if quote else latest.close
    price_change = quote.change if quote else round(change, 4)
    price_change_percent = quote.change_percent if quote else round(change / previous.close * 100, 4)
    price_timestamp = quote.timestamp if quote else latest.date
    price_provider = quote.provider if quote else "history-fallback"
    price_realtime = quote.realtime if quote else False
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
    evidence = EvidenceReport(
        historical_win_rate=accuracy.historical_win_rate,
        historical_accuracy=accuracy.historical_accuracy,
        sample_size=accuracy.matching_setups,
        statistical_confidence=accuracy.confidence_level,
        average_return=accuracy.average_return,
        average_loss=accuracy.average_drawdown,
        maximum_drawdown=round(abs(accuracy.average_drawdown) * 1.35, 2),
        profit_factor=accuracy.profit_factor,
        expected_value=accuracy.expected_return,
        best_holding_period=accuracy.best_holding_window,
    )
    rank_reason = (
        f"It ranks highly because the adaptive engine currently gives the most weight to "
        f"{_top_weight_labels(adaptive_weights)} and this setup has {accuracy.matching_setups} comparable historical cases."
    )
    explanation = (
        f"{symbol} is a {setup_stage} in a {market_regime.name.lower()} regime with a {trigger_label} near {entry:.2f}. "
        f"{rank_reason} Historical evidence shows {accuracy.historical_accuracy:.0f}% confidence-adjusted accuracy, "
        f"{accuracy.historical_win_rate:.0f}% raw win rate, {accuracy.expected_return:.2f}% expected value, "
        f"and {accuracy.profit_factor:.2f} profit factor over the best window of {accuracy.best_holding_window}. "
        f"Confirmation is {timeframe.alignment_score:.0f}/100 across weekly, daily, and intraday proxy trends, "
        f"with institutional confirmation at {institutional.confirmation_score:.0f}/100. "
        f"The invalidation level is {stop:.2f}; target is {target:.2f}; risk/reward is {risk_reward:.2f}:1. "
        f"The swing-trade filter reads {trend_label} with {volume_label} at {volume_ratio:.2f}x the recent average."
    )
    return Intelligence(
        symbol=symbol,
        category=category,
        latest_price=round(latest_price, 4),
        price_change=price_change,
        price_change_percent=price_change_percent,
        price_timestamp=price_timestamp,
        price_provider=price_provider,
        price_realtime=price_realtime,
        vol_edge_score=score,
        confidence_score=confidence_score,
        risk_score=risk_score,
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
        market_regime=market_regime,
        evidence=evidence,
        timeframe_confirmation=timeframe,
        institutional_confirmation=institutional,
        adaptive_weights=adaptive_weights,
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


def _confidence_score(
    vol_edge_score: float,
    accuracy,
    pattern_quality: float,
    timeframe_alignment: float,
    institutional_confirmation: float,
    regime_modifier: float,
) -> float:
    sample_score = min(100, accuracy.matching_setups / 80 * 100)
    score = (
        accuracy.historical_accuracy * 0.28
        + sample_score * 0.18
        + pattern_quality * 0.18
        + timeframe_alignment * 0.16
        + institutional_confirmation * 0.14
        + vol_edge_score * 0.06
        + regime_modifier
    )
    return round(min(100, max(0, score)), 2)


def _risk_score(bars, average_drawdown: float, risk_reward: float, market_regime: str) -> float:
    recent_atr = sum(bar.high - bar.low for bar in bars[-14:]) / 14
    atr_percent = recent_atr / max(0.01, bars[-1].close) * 100
    drawdown_risk = min(100, abs(average_drawdown) * 7)
    rr_risk = max(0, 60 - min(4, risk_reward) * 15)
    regime_risk = 18 if market_regime == "Crisis Mode" else 12 if market_regime in {"Bear Market", "High Volatility"} else 6
    score = atr_percent * 6 + drawdown_risk * 0.35 + rr_risk * 0.35 + regime_risk
    return round(min(100, max(0, score)), 2)


def _top_weight_labels(weights: dict[str, float]) -> str:
    labels = {
        "accuracy": "historical accuracy",
        "pattern": "pattern reliability",
        "volatility": "volatility expansion",
        "momentum": "momentum",
        "risk_reward": "risk/reward",
        "volume": "relative volume",
        "trend": "trend alignment",
        "timeframe": "multi-timeframe alignment",
        "institutional": "institutional confirmation",
    }
    top = sorted(weights.items(), key=lambda item: item[1], reverse=True)[:3]
    return ", ".join(labels.get(name, name) for name, _ in top)
