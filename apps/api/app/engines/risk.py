from __future__ import annotations

from collections import defaultdict

from ..market_data import ETF_UNIVERSE
from ..models import PortfolioRiskReport, RiskExposure


def build_portfolio_risk(symbols: list[str]) -> PortfolioRiskReport:
    buckets: dict[str, float] = defaultdict(float)
    for symbol in symbols:
        category, leverage = ETF_UNIVERSE[symbol]
        buckets[category] += max(1, abs(leverage)) * 10

    total = sum(buckets.values()) or 1
    exposures = []
    for category, raw_value in sorted(buckets.items(), key=lambda item: item[1], reverse=True):
        value = round(raw_value / total * 100, 2)
        status = "High" if value >= 40 else "Elevated" if value >= 25 else "Balanced"
        exposures.append(RiskExposure(label=category, value=value, status=status))

    dominant = exposures[0].label if exposures else "None"
    risk_score = min(100, round(sum(item.value for item in exposures[:2]) * 0.85, 2))
    return PortfolioRiskReport(
        risk_score=risk_score,
        dominant_exposure=dominant,
        correlation_watch="Leveraged ETFs and broad-market beta",
        exposures=exposures,
        guardrails=[
            "No automatic trading",
            "Manual approval required",
            "Suggested stop loss required for every alert",
        ],
    )
