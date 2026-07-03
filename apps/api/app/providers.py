from __future__ import annotations

from datetime import datetime, timezone
from typing import Protocol

import httpx

from .config import get_settings
from .market_data import load_ohlcv
from .models import OhlcvBar


class MarketDataProvider(Protocol):
    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        ...


class SampleMarketDataProvider:
    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        return load_ohlcv(symbol, bars=bars)


class PolygonMarketDataProvider:
    def __init__(self, api_key: str) -> None:
        self.api_key = _require_key(api_key, "POLYGON_API_KEY")

    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/2024-01-01/2026-12-31"
        payload = _get_json(url, {"adjusted": "true", "sort": "desc", "limit": bars, "apiKey": self.api_key})
        rows = payload.get("results", [])
        normalized = [
            OhlcvBar(
                date=_date_from_epoch_ms(row["t"]),
                open=float(row["o"]),
                high=float(row["h"]),
                low=float(row["l"]),
                close=float(row["c"]),
                volume=int(row["v"]),
            )
            for row in rows
        ]
        return list(reversed(normalized))


class TwelveDataMarketDataProvider:
    def __init__(self, api_key: str) -> None:
        self.api_key = _require_key(api_key, "TWELVE_DATA_API_KEY")

    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        payload = _get_json(
            "https://api.twelvedata.com/time_series",
            {"symbol": symbol, "interval": "1day", "outputsize": bars, "apikey": self.api_key},
        )
        rows = payload.get("values", [])
        normalized = [
            OhlcvBar(
                date=row["datetime"],
                open=float(row["open"]),
                high=float(row["high"]),
                low=float(row["low"]),
                close=float(row["close"]),
                volume=int(float(row.get("volume") or 0)),
            )
            for row in rows
        ]
        return list(reversed(normalized))


class FinnhubMarketDataProvider:
    def __init__(self, api_key: str) -> None:
        self.api_key = _require_key(api_key, "FINNHUB_API_KEY")

    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        to_timestamp = int(datetime.now(tz=timezone.utc).timestamp())
        from_timestamp = to_timestamp - bars * 3 * 86_400
        payload = _get_json(
            "https://finnhub.io/api/v1/stock/candle",
            {
                "symbol": symbol,
                "resolution": "D",
                "from": from_timestamp,
                "to": to_timestamp,
                "token": self.api_key,
            },
        )
        if payload.get("s") != "ok":
            raise ProviderNotConfiguredError(f"Finnhub did not return candle data for {symbol}.")
        rows = zip(payload["t"], payload["o"], payload["h"], payload["l"], payload["c"], payload["v"])
        normalized = [
            OhlcvBar(
                date=_date_from_epoch_seconds(timestamp),
                open=float(open_price),
                high=float(high),
                low=float(low),
                close=float(close),
                volume=int(volume),
            )
            for timestamp, open_price, high, low, close, volume in rows
        ]
        return normalized[-bars:]


class ProviderNotConfiguredError(RuntimeError):
    pass


def get_market_data_provider() -> MarketDataProvider:
    settings = get_settings()
    provider = settings.market_data_provider.lower()
    if provider in {"sample", "sample-provider-ready"}:
        return SampleMarketDataProvider()
    if provider == "polygon":
        return PolygonMarketDataProvider(settings.polygon_api_key)
    if provider in {"twelve", "twelve-data", "twelvedata"}:
        return TwelveDataMarketDataProvider(settings.twelve_data_api_key)
    if provider == "finnhub":
        return FinnhubMarketDataProvider(settings.finnhub_api_key)
    raise ProviderNotConfiguredError(
        f"{settings.market_data_provider} adapter is not configured in this build. "
        "Supported values: sample-provider-ready, polygon, twelve-data, finnhub."
    )


def _require_key(value: str, name: str) -> str:
    if not value:
        raise ProviderNotConfiguredError(f"{name} is required for the selected market data provider.")
    return value


def _get_json(url: str, params: dict[str, str | int]) -> dict:
    try:
        response = httpx.get(url, params=params, timeout=20)
        response.raise_for_status()
        payload = response.json()
    except httpx.HTTPError as exc:
        raise ProviderNotConfiguredError(f"Market data request failed: {exc}") from exc

    if not isinstance(payload, dict):
        raise ProviderNotConfiguredError("Market data provider returned an unexpected response.")
    return payload


def _date_from_epoch_ms(value: int) -> str:
    return datetime.fromtimestamp(value / 1000, tz=timezone.utc).date().isoformat()


def _date_from_epoch_seconds(value: int) -> str:
    return datetime.fromtimestamp(value, tz=timezone.utc).date().isoformat()
