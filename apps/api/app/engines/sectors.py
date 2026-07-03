from __future__ import annotations

from time import monotonic

from ..config import get_settings
from ..market_data import ETF_UNIVERSE
from ..models import Recommendation, SectorSignal
from ..providers import get_market_data_provider


SECTOR_SYMBOLS = ["XLK", "SOXX", "GLD", "SLV", "GDX", "EEM", "XLF", "XLE", "XBI", "IWM", "IBIT", "ETHA"]
CACHE_TTL_SECONDS = get_settings().cache_ttl_seconds
_sector_signal_cache: dict[str, tuple[float, SectorSignal]] = {}
_sector_radar_cache: tuple[float, list[SectorSignal]] | None = None


def calculate_sector_signal(symbol: str, force_refresh: bool = False) -> SectorSignal:
    normalized_symbol = symbol.upper()
    cached = _sector_signal_cache.get(normalized_symbol)
    now = monotonic()
    if cached and not force_refresh and now - cached[0] < CACHE_TTL_SECONDS:
        return cached[1]

    signal = _calculate_sector_signal(normalized_symbol)
    _sector_signal_cache[normalized_symbol] = (now, signal)
    return signal


def _calculate_sector_signal(symbol: str) -> SectorSignal:
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


def sector_radar(force_refresh: bool = False) -> list[SectorSignal]:
    global _sector_radar_cache

    now = monotonic()
    if _sector_radar_cache and not force_refresh and now - _sector_radar_cache[0] < CACHE_TTL_SECONDS:
        return _sector_radar_cache[1]

    ranked = sorted((calculate_sector_signal(symbol, force_refresh=force_refresh) for symbol in SECTOR_SYMBOLS), key=lambda item: item.sector_volatility_score, reverse=True)
    _sector_radar_cache = (now, ranked)
    return ranked
