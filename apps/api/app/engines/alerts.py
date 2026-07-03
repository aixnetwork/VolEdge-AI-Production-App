from __future__ import annotations

from ..models import Alert, AlertEvaluation
from ..services import build_intelligence


def evaluate_alert(alert: Alert) -> AlertEvaluation:
    intelligence = build_intelligence(alert.symbol)
    condition = alert.condition.lower()
    triggered = False

    if "score" in condition:
        triggered = intelligence.vol_edge_score >= alert.threshold
    elif "accuracy" in condition:
        triggered = intelligence.historical_accuracy >= alert.threshold
    elif "return" in condition:
        triggered = intelligence.expected_return >= alert.threshold

    reason = (
        f"{alert.symbol} meets {alert.condition} at {intelligence.vol_edge_score:.2f}"
        if triggered
        else f"{alert.symbol} has not met {alert.condition}"
    )
    return AlertEvaluation(
        symbol=alert.symbol,
        triggered=triggered,
        reason=reason,
        vol_edge_score=intelligence.vol_edge_score,
    )
