from __future__ import annotations

import math
from typing import Iterable

from .models import OhlcvBar


ETF_UNIVERSE = {
    "SPY": ("Broad Market", 1),
    "QQQ": ("Broad Market", 1),
    "DIA": ("Broad Market", 1),
    "IWM": ("Small Cap", 1),
    "UPRO": ("Broad Market", 3),
    "SPXU": ("Broad Market", -3),
    "TQQQ": ("Nasdaq 100", 3),
    "SQQQ": ("Nasdaq 100", -3),
    "XLK": ("Technology", 1),
    "XLC": ("Communications", 1),
    "XLY": ("Consumer Discretionary", 1),
    "XLP": ("Consumer Staples", 1),
    "XLV": ("Healthcare", 1),
    "XLI": ("Industrials", 1),
    "XLU": ("Utilities", 1),
    "XLB": ("Materials", 1),
    "SOXX": ("Semiconductors", 1),
    "SMH": ("Semiconductors", 1),
    "SOXL": ("Semiconductors", 3),
    "SOXS": ("Semiconductors", -3),
    "TECL": ("Technology", 3),
    "TECS": ("Technology", -3),
    "UVIX": ("Volatility", 2),
    "VIXY": ("Volatility", 1),
    "SVIX": ("Volatility", -1),
    "TLT": ("Treasury Bonds", 1),
    "TMF": ("Treasury Bonds", 3),
    "TMV": ("Treasury Bonds", -3),
    "HYG": ("Credit", 1),
    "LQD": ("Credit", 1),
    "GLD": ("Gold", 1),
    "SLV": ("Silver", 1),
    "GDX": ("Gold Miners", 1),
    "GDXJ": ("Gold Miners", 1),
    "NUGT": ("Gold Miners", 2),
    "DUST": ("Gold Miners", -2),
    "EEM": ("Emerging Markets", 1),
    "EEV": ("Emerging Markets", -2),
    "EDC": ("Emerging Markets", 3),
    "EDZ": ("Emerging Markets", -3),
    "XLF": ("Financials", 1),
    "FAS": ("Financials", 3),
    "FAZ": ("Financials", -3),
    "KRE": ("Regional Banks", 1),
    "XLE": ("Energy", 1),
    "ERX": ("Energy", 2),
    "ERY": ("Energy", -2),
    "USO": ("Oil", 1),
    "UNG": ("Natural Gas", 1),
    "XBI": ("Biotech", 1),
    "LABU": ("Biotech", 3),
    "LABD": ("Biotech", -3),
    "XRT": ("Retail", 1),
    "URA": ("Uranium", 1),
    "TAN": ("Solar", 1),
    "ICLN": ("Clean Energy", 1),
    "TNA": ("Small Cap", 3),
    "TZA": ("Small Cap", -3),
    "IBIT": ("Crypto Bitcoin", 1),
    "FBTC": ("Crypto Bitcoin", 1),
    "BITB": ("Crypto Bitcoin", 1),
    "ARKB": ("Crypto Bitcoin", 1),
    "GBTC": ("Crypto Bitcoin", 1),
    "HODL": ("Crypto Bitcoin", 1),
    "BITO": ("Bitcoin Futures", 1),
    "BITU": ("Leveraged Bitcoin", 2),
    "SBIT": ("Inverse Bitcoin", -2),
    "ETHA": ("Crypto Ethereum", 1),
    "FETH": ("Crypto Ethereum", 1),
    "ETHW": ("Crypto Ethereum", 1),
    "ETHE": ("Crypto Ethereum", 1),
}


def load_ohlcv(symbol: str, bars: int = 140) -> list[OhlcvBar]:
    """Deterministic provider-ready sample data.

    Production adapters should replace this function with licensed OHLCV from
    Polygon, Twelve Data, Finnhub, or another approved data vendor.
    """
    if symbol not in ETF_UNIVERSE:
        raise KeyError(f"Unsupported ETF symbol: {symbol}")

    category, leverage = ETF_UNIVERSE[symbol]
    seed = sum(ord(char) for char in symbol)
    base = 24 + seed % 95
    trend = 0.055 * (1 if leverage >= 0 else -1)
    volatility = 0.9 + abs(leverage) * 0.42 + (seed % 7) * 0.08
    series: list[OhlcvBar] = []

    for i in range(bars):
        wave = math.sin((i + seed) / 6) * volatility
        acceleration = max(0, i - bars + 26) * 0.18 * (1 if leverage >= 0 else -1)
        close = base + i * trend + wave + acceleration
        open_price = close - math.sin((i + seed) / 4) * 0.45
        high = max(open_price, close) + volatility * (1.05 + (i % 4) * 0.08)
        low = min(open_price, close) - volatility * (0.95 + (i % 3) * 0.07)
        volume = int(1_200_000 + (seed % 23) * 72_000 + i * 14_000 + max(0, i - bars + 18) * 82_000)
        series.append(
            OhlcvBar(
                date=f"2026-02-{(i % 28) + 1:02d}",
                open=round(open_price, 2),
                high=round(high, 2),
                low=round(low, 2),
                close=round(close, 2),
                volume=volume,
            )
        )
    return series


def returns(bars: Iterable[OhlcvBar], holding_period: int = 5) -> list[float]:
    values = list(bars)
    return [
        (values[i + holding_period].close - values[i].close) / values[i].close
        for i in range(0, len(values) - holding_period)
    ]
