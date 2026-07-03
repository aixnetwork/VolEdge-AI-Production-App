from __future__ import annotations

from ..models import MarketRegime, OhlcvBar


def classify_market_regime(spy: list[OhlcvBar], qqq: list[OhlcvBar], volatility: list[OhlcvBar] | None = None) -> MarketRegime:
    spy_trend = _trend_percent(spy, 50)
    qqq_trend = _trend_percent(qqq, 50)
    spy_short = _trend_percent(spy, 20)
    atr_ratio = _atr_ratio(spy)
    vol_trend = _trend_percent(volatility, 20) if volatility else 0

    if atr_ratio >= 1.45 and vol_trend > 12 and spy_short < -4:
        regime = "Crisis Mode"
        risk_bias = "Risk-Off"
        confidence_modifier = -8
    elif atr_ratio >= 1.25 or vol_trend > 10:
        regime = "High Volatility"
        risk_bias = "Risk-Off" if spy_short < 0 else "Risk-On"
        confidence_modifier = -2 if spy_short < 0 else 1
    elif spy_trend > 4 and qqq_trend > 4:
        regime = "Bull Market"
        risk_bias = "Risk-On"
        confidence_modifier = 5
    elif spy_trend < -4 and qqq_trend < -4:
        regime = "Bear Market"
        risk_bias = "Risk-Off"
        confidence_modifier = -4
    elif atr_ratio <= 0.78:
        regime = "Low Volatility"
        risk_bias = "Risk-On" if spy_short >= 0 else "Risk-Off"
        confidence_modifier = 1
    else:
        regime = "Sideways Market"
        risk_bias = "Neutral"
        confidence_modifier = -1

    return MarketRegime(
        name=regime,
        risk_bias=risk_bias,
        volatility_state="High" if atr_ratio >= 1.15 else "Low" if atr_ratio <= 0.85 else "Normal",
        confidence_modifier=confidence_modifier,
        evidence=f"SPY 50-bar trend {spy_trend:.1f}%, QQQ 50-bar trend {qqq_trend:.1f}%, ATR regime {atr_ratio:.2f}x.",
    )


def _trend_percent(bars: list[OhlcvBar] | None, lookback: int) -> float:
    if not bars or len(bars) <= lookback:
        return 0
    return (bars[-1].close / bars[-lookback].close - 1) * 100


def _atr_ratio(bars: list[OhlcvBar]) -> float:
    recent = bars[-14:]
    prior = bars[-70:-14]
    recent_atr = sum(bar.high - bar.low for bar in recent) / len(recent)
    prior_atr = sum(bar.high - bar.low for bar in prior) / max(1, len(prior))
    return recent_atr / max(0.01, prior_atr)
