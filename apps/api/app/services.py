from __future__ import annotations

from time import monotonic

from .config import get_settings
from .engines.accuracy import calculate_historical_accuracy
from .engines.confirmation import build_institutional_confirmation, build_timeframe_confirmation
from .engines.market_regime import classify_market_regime
from .engines.patterns import detect_primary_pattern
from .engines.voledge_score import adaptive_factor_weights, score_opportunity
from .market_data import ETF_UNIVERSE
from .models import EvidenceReport, Intelligence, PatternSignal, Recommendation, SwingTransitionSignal
from .providers import get_market_data_provider


RADAR_PRIORITY_SYMBOLS = [
    "SPY",
    "QQQ",
    "IWM",
    "UPRO",
    "SPXU",
    "TQQQ",
    "SQQQ",
    "XLK",
    "XLC",
    "XLY",
    "XLP",
    "XLV",
    "XLI",
    "XLU",
    "XLB",
    "SOXX",
    "SMH",
    "SOXL",
    "SOXS",
    "TECL",
    "TECS",
    "UVIX",
    "VIXY",
    "SVIX",
    "TLT",
    "TMF",
    "TMV",
    "HYG",
    "LQD",
    "GLD",
    "SLV",
    "GDX",
    "XLF",
    "KRE",
    "XLE",
    "USO",
    "UNG",
    "XBI",
    "LABU",
    "LABD",
    "XRT",
    "URA",
    "TAN",
    "ICLN",
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

settings = get_settings()
CACHE_TTL_SECONDS = settings.cache_ttl_seconds
MIN_TRADE_READY_ACCURACY = 60
MIN_TRADE_READY_MATCHES = 10
MIN_TRADE_READY_PROFIT_FACTOR = 1.1
MIN_TRADE_READY_RISK_REWARD = 1.35
_intelligence_cache: dict[str, tuple[float, Intelligence]] = {}
_radar_cache: tuple[float, list[Intelligence]] | None = None


def build_intelligence(symbol: str, force_refresh: bool = False) -> Intelligence:
    normalized_symbol = symbol.upper()
    cached = _intelligence_cache.get(normalized_symbol)
    now = monotonic()
    if cached and not force_refresh and now - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]

    intelligence = _build_intelligence(normalized_symbol)
    _intelligence_cache[normalized_symbol] = (now, intelligence)
    return intelligence


def _build_intelligence(symbol: str) -> Intelligence:
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
        stop = min(resistance, entry + atr * 1.05) if resistance > entry else entry + atr * 1.05
        target = entry - atr * 2.0
    else:
        entry = max(latest.close, resistance + atr * 0.08) if pattern.name.startswith("Pre-Breakout") else latest.close
        stop = max(support, entry - atr * 1.05) if support < entry else entry - atr * 1.05
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
    risk_reward = abs(target - entry) / max(0.01, abs(entry - stop))
    quality_gate = _trade_quality_gate(accuracy, risk_reward)
    if not quality_gate["passed"]:
        score = min(score, float(quality_gate["score_cap"]))
        confidence_score = min(confidence_score, score)
    if pattern.direction == "Neutral":
        score = min(score, 64.0)
        confidence_score = min(confidence_score, score)
    risk_score = _risk_score(bars, accuracy.average_drawdown, risk_reward=risk_reward, market_regime=market_regime.name)
    pattern = _augment_pattern_prediction(pattern, accuracy.historical_accuracy, timeframe.alignment_score, institutional.confirmation_score, confidence_score)
    transition_entry = _next_transition_trigger(latest.close, entry, atr, pattern.direction, pattern.name)
    swing_transition = _swing_transition_signal(
        latest_close=latest.close,
        entry=transition_entry,
        stop=stop,
        pattern_direction=pattern.direction,
        accuracy=accuracy.historical_accuracy,
        confidence_score=confidence_score,
        timeframe_alignment=timeframe.alignment_score,
        institutional_confirmation=institutional.confirmation_score,
    )
    if not quality_gate["passed"]:
        recommendation = Recommendation.WATCH
    elif pattern.direction == "Bearish":
        recommendation = Recommendation.STRONG_SELL if score >= 73 else Recommendation.HEDGE if score >= 62 else Recommendation.WATCH
    elif pattern.direction == "Neutral":
        recommendation = Recommendation.WATCH
    else:
        recommendation = Recommendation.EXTREME_BUY if score >= 85 else Recommendation.STRONG_BUY if score >= 73 else Recommendation.WATCH
    confidence_level = "Very High" if score >= 88 and accuracy.historical_accuracy >= 65 else pattern.confidence_level
    if not quality_gate["passed"]:
        confidence_level = "Low" if accuracy.historical_accuracy < MIN_TRADE_READY_ACCURACY else "Medium"
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
    gate_note = (
        ""
        if quality_gate["passed"]
        else f" The trade-quality gate keeps this on Watch because {quality_gate['reason']}."
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
        f"{gate_note}"
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
        swing_transition=swing_transition,
        adaptive_weights=adaptive_weights,
        ai_explanation=explanation,
    )


def opportunity_radar(force_refresh: bool = False) -> list[Intelligence]:
    global _radar_cache

    now = monotonic()
    if _radar_cache and not force_refresh and now - _radar_cache[0] < CACHE_TTL_SECONDS:
        return _radar_cache[1]

    opportunities = []
    for symbol in RADAR_PRIORITY_SYMBOLS:
        if symbol not in ETF_UNIVERSE:
            continue
        try:
            opportunities.append(build_intelligence(symbol, force_refresh=force_refresh))
        except Exception:
            continue
    if not opportunities:
        opportunities = [build_intelligence(symbol) for symbol in ("SPY", "QQQ", "GLD")]
    ranked = sorted(opportunities, key=lambda item: item.vol_edge_score, reverse=True)
    _radar_cache = (now, ranked)
    return ranked


def warm_intelligence_cache() -> dict[str, int | float | str]:
    started = monotonic()
    opportunities = opportunity_radar(force_refresh=True)
    return {
        "status": "warm",
        "symbols": len(opportunities),
        "top_symbol": opportunities[0].symbol if opportunities else "",
        "elapsed_ms": round((monotonic() - started) * 1000),
        "cache_ttl_seconds": CACHE_TTL_SECONDS,
    }


def intelligence_cache_status() -> dict[str, int | float | bool]:
    now = monotonic()
    radar_age = round(now - _radar_cache[0], 2) if _radar_cache else None
    return {
        "cache_ttl_seconds": CACHE_TTL_SECONDS,
        "radar_ready": _radar_cache is not None,
        "radar_age_seconds": radar_age,
        "intelligence_symbols": len(_intelligence_cache),
    }


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


def _trade_quality_gate(accuracy, risk_reward: float) -> dict[str, bool | float | str]:
    blockers: list[str] = []
    if accuracy.historical_accuracy < MIN_TRADE_READY_ACCURACY:
        blockers.append(f"qualified accuracy is {accuracy.historical_accuracy:.0f}%")
    if accuracy.matching_setups < MIN_TRADE_READY_MATCHES:
        blockers.append(f"only {accuracy.matching_setups} historical matches are available")
    if accuracy.profit_factor < MIN_TRADE_READY_PROFIT_FACTOR:
        blockers.append(f"profit factor is {accuracy.profit_factor:.2f}")
    if accuracy.expected_return <= 0:
        blockers.append(f"expected value is {accuracy.expected_return:.2f}%")
    if risk_reward < MIN_TRADE_READY_RISK_REWARD:
        blockers.append(f"risk/reward is {risk_reward:.2f}:1")

    if not blockers:
        return {"passed": True, "score_cap": 100.0, "reason": "qualified setup passes trade-ready filters"}

    hard_block = accuracy.historical_accuracy < 52 or accuracy.expected_return <= 0 or accuracy.profit_factor < 1
    score_cap = 54.0 if hard_block else 62.0
    return {"passed": False, "score_cap": score_cap, "reason": "; ".join(blockers)}


def _augment_pattern_prediction(
    pattern: PatternSignal,
    historical_accuracy: float,
    timeframe_alignment: float,
    institutional_confirmation: float,
    confidence_score: float,
) -> PatternSignal:
    analog_score = pattern.analog_confidence if pattern.analog_count >= 8 else pattern.prediction_score
    prediction_score = (
        pattern.chart_score * 0.34
        + analog_score * 0.20
        + historical_accuracy * 0.16
        + timeframe_alignment * 0.14
        + institutional_confirmation * 0.10
        + confidence_score * 0.06
    )
    prediction_score = round(min(100, max(0, prediction_score)), 2)
    if pattern.direction == "Bullish":
        breakout_probability = max(pattern.breakout_probability, prediction_score)
        breakdown_probability = min(pattern.breakdown_probability, max(0, 100 - prediction_score - 8))
    elif pattern.direction == "Bearish":
        breakdown_probability = max(pattern.breakdown_probability, prediction_score)
        breakout_probability = min(pattern.breakout_probability, max(0, 100 - prediction_score - 8))
    else:
        breakout_probability = breakdown_probability = min(54, prediction_score * 0.62)
    evidence = [
        *pattern.evidence,
        f"multi-timeframe alignment {timeframe_alignment:.0f}/100",
        f"institutional confirmation {institutional_confirmation:.0f}/100",
    ]
    if pattern.analog_count >= 8:
        evidence.append(f"AI analog confidence {pattern.analog_confidence:.0f}/100")
    return pattern.model_copy(
        update={
            "prediction_score": prediction_score,
            "breakout_probability": round(breakout_probability, 2),
            "breakdown_probability": round(breakdown_probability, 2),
            "evidence": evidence[:7],
        }
    )


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


def _swing_transition_signal(
    latest_close: float,
    entry: float,
    stop: float,
    pattern_direction: str,
    accuracy: float,
    confidence_score: float,
    timeframe_alignment: float,
    institutional_confirmation: float,
) -> SwingTransitionSignal:
    if pattern_direction == "Neutral":
        return SwingTransitionSignal(
            action="Hold",
            status="Waiting",
            transition_score=0,
            trigger_price=round(latest_close, 2),
            trigger_gap_percent=0,
            reason="No directional transition is active yet.",
        )

    if pattern_direction == "Bearish":
        action = "Hold -> Sell"
        trigger_gap = (latest_close - entry) / max(0.01, latest_close) * 100
        triggered = latest_close <= entry
        invalidated = latest_close >= stop
        direction_word = "sell"
    else:
        action = "Hold -> Buy"
        trigger_gap = (entry - latest_close) / max(0.01, latest_close) * 100
        triggered = latest_close >= entry
        invalidated = latest_close <= stop
        direction_word = "buy"

    proximity_score = max(0, 100 - min(100, abs(trigger_gap) * 32))
    transition_score = (
        accuracy * 0.38
        + confidence_score * 0.22
        + timeframe_alignment * 0.14
        + institutional_confirmation * 0.14
        + proximity_score * 0.12
    )
    if invalidated:
        status = "Invalidated"
    elif triggered:
        status = "Triggered"
    elif transition_score >= 68 and accuracy >= 60 and abs(trigger_gap) <= 2.8:
        status = "Arming"
    else:
        status = "Waiting"

    reason = (
        f"Hold until the {direction_word} trigger confirms. "
        f"The setup is {abs(trigger_gap):.2f}% from trigger with {accuracy:.0f}% historical accuracy "
        f"and {confidence_score:.0f}/100 confidence."
    )
    return SwingTransitionSignal(
        action=action,
        status=status,
        transition_score=round(min(100, max(0, transition_score)), 2),
        trigger_price=round(entry, 2),
        trigger_gap_percent=round(trigger_gap, 2),
        reason=reason,
    )


def _next_transition_trigger(latest_close: float, suggested_entry: float, atr: float, direction: str, pattern_name: str) -> float:
    if pattern_name.startswith("Pre-"):
        return suggested_entry
    if direction == "Bearish":
        return min(suggested_entry, latest_close - atr * 0.35)
    if direction == "Bullish":
        return max(suggested_entry, latest_close + atr * 0.35)
    return latest_close
