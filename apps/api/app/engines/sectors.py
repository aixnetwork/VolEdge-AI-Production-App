from __future__ import annotations

from ..market_data import ETF_UNIVERSE
from ..models import Recommendation, SectorSignal
from ..providers import get_market_data_provider


SECTOR_SYMBOLS = ["XLK", "SOXX", "GLD", "SLV", "GDX", "EEM", "XLF", "XLE", "XBI", "IWM", "IBIT", "ETHA"]


def calculate_sector_signal(symbol: str) -> SectorSignal:
    provider = get_market_data_provider()
    bars = provider.history(symbol)
    spy = provider.history("SPY")
    recent = bars[-14:]
    prior = bars[-42:-14]
    atr_recent = sum(bar.high - bar.low for bar in recent) / len(recent)
    atr_prior = sum(bar.high - bar.low for bar in prior) / len(prior)
    atr_expansion = min(100, atr_recent / atr_prior * 72)

    realized_vol = min(100, abs(bars[-1].close - bars[-15].close) / bars[-15].close * 900)
    volume_surge = min(100, bars[-1].volume / (sum(bar.volume for bar in prior) / len(prior)) * 55)
    breakout = 100 if bars[-1].close > max(bar.high for bar in prior) else 45
    relative_strength = min(100, max(0, ((bars[-1].close / bars[-20].close) - (spy[-1].close / spy[-20].close)) * 800 + 50))
    score = atr_expansion * 0.30 + realized_vol * 0.25 + volume_surge * 0.20 + breakout * 0.15 + relative_strength * 0.10

    if score >= 82:
        recommendation = Recommendation.EXTREME_BUY
    elif score >= 70:
        recommendation = Recommendation.STRONG_BUY
    elif score <= 38:
        recommendation = Recommendation.STRONG_SELL
    elif relative_strength < 35 and score >= 55:
        recommendation = Recommendation.HEDGE
    else:
        recommendation = Recommendation.WATCH

    return SectorSignal(
        sector=ETF_UNIVERSE[symbol][0],
        symbol=symbol,
        sector_volatility_score=round(score, 2),
        recommendation=recommendation,
        atr_expansion=round(atr_expansion, 2),
        realized_volatility_spike=round(realized_vol, 2),
        volume_surge=round(volume_surge, 2),
        relative_strength_vs_spy=round(relative_strength, 2),
    )


def sector_radar() -> list[SectorSignal]:
    return sorted((calculate_sector_signal(symbol) for symbol in SECTOR_SYMBOLS), key=lambda item: item.sector_volatility_score, reverse=True)
