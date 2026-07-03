from __future__ import annotations

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .engines.accuracy import calculate_historical_accuracy
from .engines.alerts import evaluate_alert
from .engines.backtesting import run_signal_backtest, summarize_backtest_windows
from .engines.patterns import detect_primary_pattern
from .engines.risk import build_portfolio_risk
from .engines.sectors import calculate_sector_signal, sector_radar
from .market_data import ETF_UNIVERSE
from .models import Alert, AlertCreate, WatchlistAdd
from .providers import ProviderNotConfiguredError, get_market_data_provider
from .services import build_intelligence, intelligence_cache_status, opportunity_radar, warm_intelligence_cache
from .storage import store

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Alert-only ETF intelligence API for VolEdge AI.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.exception_handler(ProviderNotConfiguredError)
def provider_not_configured_handler(_: Request, exc: ProviderNotConfiguredError) -> JSONResponse:
    return JSONResponse(status_code=503, content={"detail": str(exc), "trading_enabled": False})

@app.get("/api/status")
def status() -> dict[str, str | bool | list[str]]:
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "market_data": settings.market_data_provider,
        "store_backend": settings.store_backend,
        "trading_enabled": settings.trading_enabled,
        "cache_ttl_seconds": settings.cache_ttl_seconds,
        "cors_origins": settings.cors_origins,
    }


@app.get("/api/cache/status")
def cache_status():
    return intelligence_cache_status()


@app.get("/api/cache/warm")
def cache_warm():
    intelligence_status = warm_intelligence_cache()
    sectors = sector_radar(force_refresh=True)
    return {
        **intelligence_status,
        "sector_symbols": len(sectors),
        "top_sector_symbol": sectors[0].symbol if sectors else "",
    }


@app.get("/api/radar")
def radar():
    opportunities = opportunity_radar()
    return {"top_opportunity": opportunities[0], "opportunities": opportunities[:12]}


@app.get("/api/intelligence/{symbol}")
def intelligence(symbol: str):
    return _require_symbol(symbol, build_intelligence)


@app.get("/api/market/quote/{symbol}")
def market_quote(symbol: str):
    return _require_symbol(symbol, lambda value: get_market_data_provider().quote(value))


@app.get("/api/market/history/{symbol}")
def market_history(symbol: str, bars: int = 140):
    normalized_bars = max(2, min(bars, 1000))
    return _require_symbol(
        symbol,
        lambda value: {"symbol": value, "bars": get_market_data_provider().history(value, bars=normalized_bars)},
    )


@app.get("/api/patterns/{symbol}")
def patterns(symbol: str):
    def build(value: str):
        bars = get_market_data_provider().history(value)
        accuracy = calculate_historical_accuracy(bars, quality_threshold=0.012)
        return detect_primary_pattern(bars, accuracy.historical_accuracy)

    return _require_symbol(symbol, build)


@app.get("/api/accuracy/{symbol}")
def accuracy(symbol: str):
    return _require_symbol(symbol, lambda value: calculate_historical_accuracy(get_market_data_provider().history(value), quality_threshold=0.012))


@app.get("/api/backtest/{symbol}")
def backtest(symbol: str):
    intel = _require_symbol(symbol, build_intelligence)
    return {"summary": run_signal_backtest(intel), "windows": summarize_backtest_windows(intel.symbol)}


@app.get("/api/sectors/radar")
def sectors_radar():
    return {"sectors": sector_radar()}


@app.get("/api/sectors/{sector}")
def sector_detail(sector: str):
    matches = [symbol for symbol, (category, _) in ETF_UNIVERSE.items() if category.lower().replace(" ", "-") == sector.lower()]
    if not matches:
        raise HTTPException(status_code=404, detail="Unknown sector")
    return {"sector": sector, "signals": [calculate_sector_signal(symbol) for symbol in matches[:3]]}


@app.get("/api/alerts")
def get_alerts():
    alerts = store.list_alerts()
    return {"alerts": alerts, "evaluations": [evaluate_alert(alert) for alert in alerts]}


@app.post("/api/alerts")
def create_alert(alert: AlertCreate):
    _ensure_symbol(alert.symbol)
    saved = Alert(id=f"alert_{len(store.list_alerts()) + 1}", **alert.model_dump())
    return store.create_alert(saved)


@app.get("/api/watchlist")
def get_watchlist():
    watchlist = store.list_watchlist()
    return {"symbols": watchlist, "opportunities": [build_intelligence(symbol) for symbol in watchlist]}


@app.post("/api/watchlist")
def add_watchlist(item: WatchlistAdd):
    symbol = _ensure_symbol(item.symbol)
    return {"symbols": store.add_watchlist_symbol(symbol)}


@app.get("/api/risk")
def portfolio_risk():
    return build_portfolio_risk(store.list_watchlist())


def _ensure_symbol(symbol: str) -> str:
    value = symbol.strip().upper()
    if value not in ETF_UNIVERSE:
        raise HTTPException(status_code=404, detail="Unknown ETF symbol")
    return value


def _require_symbol(symbol: str, builder):
    return builder(_ensure_symbol(symbol))
