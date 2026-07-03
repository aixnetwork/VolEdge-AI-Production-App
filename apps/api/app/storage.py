from __future__ import annotations

import uuid
from typing import Protocol

import httpx

from .config import get_settings
from .models import Alert


class AppStore(Protocol):
    def list_alerts(self) -> list[Alert]:
        ...

    def create_alert(self, alert: Alert) -> Alert:
        ...

    def list_watchlist(self) -> list[str]:
        ...

    def add_watchlist_symbol(self, symbol: str) -> list[str]:
        ...


class InMemoryStore:
    def __init__(self) -> None:
        self._alerts: list[Alert] = [
            Alert(id="alert_uvix_score", symbol="UVIX", condition="VolEdge Score above", threshold=82),
        ]
        self._watchlist = ["UVIX", "GLD", "SOXL", "XBI"]

    def list_alerts(self) -> list[Alert]:
        return list(self._alerts)

    def create_alert(self, alert: Alert) -> Alert:
        self._alerts.append(alert)
        return alert

    def list_watchlist(self) -> list[str]:
        return list(self._watchlist)

    def add_watchlist_symbol(self, symbol: str) -> list[str]:
        if symbol not in self._watchlist:
            self._watchlist.append(symbol)
        return self.list_watchlist()


class SupabaseRestStore:
    def __init__(self, url: str, service_role_key: str) -> None:
        if not url or not service_role_key:
            raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required for STORE_BACKEND=supabase.")
        self.url = url.rstrip("/")
        self.headers = {
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }

    def list_alerts(self) -> list[Alert]:
        rows = self._request("GET", "/rest/v1/alerts?select=id,symbol,condition,threshold,active&active=eq.true")
        return [
            Alert(
                id=str(row["id"]),
                symbol=row["symbol"],
                condition=row["condition"],
                threshold=float(row["threshold"]),
                active=bool(row.get("active", True)),
            )
            for row in rows
        ]

    def create_alert(self, alert: Alert) -> Alert:
        payload = {
            "id": alert.id if _looks_like_uuid(alert.id) else str(uuid.uuid4()),
            "symbol": alert.symbol,
            "condition": alert.condition,
            "threshold": alert.threshold,
            "active": alert.active,
        }
        rows = self._request("POST", "/rest/v1/alerts", json=payload)
        row = rows[0] if rows else payload
        return Alert(
            id=str(row["id"]),
            symbol=row["symbol"],
            condition=row["condition"],
            threshold=float(row["threshold"]),
            active=bool(row.get("active", True)),
        )

    def list_watchlist(self) -> list[str]:
        rows = self._request("GET", "/rest/v1/watchlist_items?select=symbol")
        return [row["symbol"] for row in rows]

    def add_watchlist_symbol(self, symbol: str) -> list[str]:
        self._request("POST", "/rest/v1/watchlist_items", json={"symbol": symbol})
        return self.list_watchlist()

    def _request(self, method: str, path: str, json: dict | None = None) -> list[dict]:
        response = httpx.request(method, f"{self.url}{path}", headers=self.headers, json=json, timeout=20)
        response.raise_for_status()
        if response.status_code == 204 or not response.content:
            return []
        payload = response.json()
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            return [payload]
        raise RuntimeError("Supabase returned an unexpected response.")


def build_store() -> AppStore:
    settings = get_settings()
    if settings.store_backend.lower() == "supabase":
        return SupabaseRestStore(settings.supabase_url, settings.supabase_service_role_key)
    return InMemoryStore()


def _looks_like_uuid(value: str) -> bool:
    try:
        uuid.UUID(value)
    except ValueError:
        return False
    return True


store: AppStore = build_store()
