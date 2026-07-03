from __future__ import annotations

from .engines.accuracy import calculate_historical_accuracy
from .engines.patterns import detect_primary_pattern
from .engines.voledge_score import score_opportunity
from .market_data import ETF_UNIVERSE
from .models import Intelligence, Recommendation
from .providers import get_market_data_provider


def build_intelligence(symbol: str) -> Intelligence:
    bars = get_market_data_provider().history(symbol)
    accuracy = calculate_historical_accuracy(bars, quality_threshold=0.012)
    pattern = detect_primary_pattern(bars, accuracy.historical_accuracy)
    latest = bars[-1]
    atr = sum(bar.high - bar.low for bar in bars[-14:]) / 14
    entry = latest.close
    stop = entry - atr * 1.15
    target = entry + atr * 2.2
    score = score_opportunity(bars, accuracy, pattern, entry, stop, target)
    recommendation = Recommendation.EXTREME_BUY if score >= 85 else Recommendation.STRONG_BUY if score >= 73 else Recommendation.WATCH
    confidence_level = "Very High" if score >= 88 and accuracy.historical_accuracy >= 65 else pattern.confidence_level
    risk_reward = (target - entry) / max(0.01, entry - stop)
    category = ETF_UNIVERSE[symbol][0]
    explanation = (
        f"{symbol} ranks highly because its {pattern.name.lower()} setup has a "
        f"{pattern.quality_score:.0f}/100 pattern quality score, {accuracy.historical_accuracy:.0f}% "
        f"historical accuracy across {accuracy.matching_setups} matching setups, and a calculated "
        f"{accuracy.expected_return:.2f}% expected return over the best window."
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
    return sorted((build_intelligence(symbol) for symbol in ETF_UNIVERSE), key=lambda item: item.vol_edge_score, reverse=True)
