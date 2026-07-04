from __future__ import annotations

from datetime import datetime, timezone
import math
from typing import Protocol

import httpx

from .config import get_settings
from .market_data import load_ohlcv
from .models import MarketQuote, OhlcvBar


class MarketDataProvider(Protocol):
    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        ...

    def quote(self, symbol: str) -> MarketQuote:
        ...


class SampleMarketDataProvider:
    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        return load_ohlcv(symbol, bars=bars)

    def quote(self, symbol: str) -> MarketQuote:
        bars = self.history(symbol)
        latest = bars[-1]
        previous = bars[-2]
        change = latest.close - previous.close
        return MarketQuote(
            symbol=symbol,
            price=latest.close,
            previous_close=previous.close,
            change=round(change, 4),
            change_percent=round(change / previous.close * 100, 4),
            volume=latest.volume,
            timestamp=latest.date,
            provider="sample-provider-ready",
            realtime=False,
        )


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

    def quote(self, symbol: str) -> MarketQuote:
        trade_payload = _get_json(f"https://api.polygon.io/v2/last/trade/{symbol}", {"apiKey": self.api_key})
        trade = trade_payload.get("results") or {}
        if "p" not in trade:
            raise ProviderNotConfiguredError(f"Polygon did not return a last trade for {symbol}.")

        previous_close = self.history(symbol, bars=2)[-2].close
        price = float(trade["p"])
        change = price - previous_close
        return MarketQuote(
            symbol=symbol,
            price=price,
            previous_close=previous_close,
            change=round(change, 4),
            change_percent=round(change / previous_close * 100, 4),
            volume=int(float(trade.get("s") or 0)) or None,
            timestamp=_timestamp_from_polygon_ns(trade.get("t")),
            provider="polygon",
            realtime=True,
        )


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

    def quote(self, symbol: str) -> MarketQuote:
        payload = _get_json("https://api.twelvedata.com/quote", {"symbol": symbol, "apikey": self.api_key})
        price = _first_float(payload, "close", "price")
        previous_close = _optional_float(payload, "previous_close")
        change = _optional_float(payload, "change")
        change_percent = _optional_float(payload, "percent_change")
        return MarketQuote(
            symbol=symbol,
            price=price,
            previous_close=previous_close,
            change=change,
            change_percent=change_percent,
            volume=_optional_int(payload, "volume"),
            timestamp=str(payload.get("timestamp") or payload.get("datetime") or datetime.now(tz=timezone.utc).isoformat()),
            provider="twelve-data",
            realtime=True,
        )


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

    def quote(self, symbol: str) -> MarketQuote:
        payload = _get_json("https://finnhub.io/api/v1/quote", {"symbol": symbol, "token": self.api_key})
        price = _first_float(payload, "c")
        previous_close = _optional_float(payload, "pc")
        return MarketQuote(
            symbol=symbol,
            price=price,
            previous_close=previous_close,
            change=_optional_float(payload, "d"),
            change_percent=_optional_float(payload, "dp"),
            timestamp=_date_from_epoch_seconds(int(payload["t"])) if payload.get("t") else datetime.now(tz=timezone.utc).isoformat(),
            provider="finnhub",
            realtime=True,
        )


class YFinanceMarketDataProvider:
    def history(self, symbol: str, bars: int = 140) -> list[OhlcvBar]:
        yf = _import_yfinance()
        ticker = yf.Ticker(symbol)
        frame = ticker.history(period="5y", interval="1d", auto_adjust=True)
        if frame.empty:
            raise ProviderNotConfiguredError(f"yfinance did not return daily bars for {symbol}.")

        rows = frame.tail(bars).reset_index()
        normalized = [
            OhlcvBar(
                date=str(row["Date"].date() if hasattr(row["Date"], "date") else row["Date"])[:10],
                open=round(float(row["Open"]), 4),
                high=round(float(row["High"]), 4),
                low=round(float(row["Low"]), 4),
                close=round(float(row["Close"]), 4),
                volume=int(float(row.get("Volume") or 0)),
            )
            for _, row in rows.iterrows()
        ]
        return normalized

    def quote(self, symbol: str) -> MarketQuote:
        yf = _import_yfinance()
        volume = None
        try:
            fast_info = yf.Ticker(symbol).fast_info
            price = float(fast_info.get("last_price") or fast_info.get("regular_market_price") or 0)
            previous_close = fast_info.get("previous_close")
            raw_volume = fast_info.get("last_volume")
            volume = int(float(raw_volume)) if raw_volume else None
        except Exception:
            price = 0
            previous_close = None

        if not _is_valid_number(price) or not _is_valid_number(previous_close):
            bars = self.history(symbol, bars=2)
            price = bars[-1].close
            previous_close = previous_close or bars[-2].close
            volume = volume or bars[-1].volume

        previous = float(previous_close) if previous_close else None
        change = price - previous if previous else None
        return MarketQuote(
            symbol=symbol,
            price=round(price, 4),
            previous_close=round(previous, 4) if previous else None,
            change=round(change, 4) if change is not None else None,
            change_percent=round(change / previous * 100, 4) if change is not None and previous else None,
            volume=volume,
            timestamp=datetime.now(tz=timezone.utc).isoformat(),
            provider="yfinance",
            realtime=False,
        )


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
    if provider in {"yfinance", "yahoo", "yahoo-finance"}:
        return YFinanceMarketDataProvider()
    raise ProviderNotConfiguredError(
        f"{settings.market_data_provider} adapter is not configured in this build. "
        "Supported values: sample-provider-ready, yfinance, polygon, twelve-data, finnhub."
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


def _timestamp_from_polygon_ns(value: int | None) -> str:
    if not value:
        return datetime.now(tz=timezone.utc).isoformat()
    return datetime.fromtimestamp(value / 1_000_000_000, tz=timezone.utc).isoformat()


def _first_float(payload: dict, *keys: str) -> float:
    for key in keys:
        value = payload.get(key)
        if value not in {None, ""}:
            return float(value)
    raise ProviderNotConfiguredError("Market data provider did not return a current price.")


def _optional_float(payload: dict, key: str) -> float | None:
    value = payload.get(key)
    return None if value in {None, ""} else float(value)


def _optional_int(payload: dict, key: str) -> int | None:
    value = payload.get(key)
    return None if value in {None, ""} else int(float(value))


def _is_valid_number(value: object) -> bool:
    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return False
    return math.isfinite(numeric) and numeric > 0


def _import_yfinance():
    try:
        import yfinance as yf
    except ImportError as exc:
        raise ProviderNotConfiguredError("yfinance is not installed. Add yfinance to the API requirements.") from exc
    return yf
