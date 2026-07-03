from apps.api.app.engines.accuracy import calculate_historical_accuracy
from apps.api.app.engines.alerts import evaluate_alert
from apps.api.app.engines.backtesting import run_signal_backtest
from apps.api.app.engines.patterns import detect_primary_pattern
from apps.api.app.engines.risk import build_portfolio_risk
from apps.api.app.engines.sectors import sector_radar
from apps.api.app.engines.voledge_score import score_opportunity
from apps.api.app.market_data import load_ohlcv
from apps.api.app.models import Alert
from apps.api.app.providers import FinnhubMarketDataProvider, PolygonMarketDataProvider, ProviderNotConfiguredError, TwelveDataMarketDataProvider
from apps.api.app.services import build_intelligence
from apps.api.app.services import opportunity_radar
from apps.api.app.storage import InMemoryStore


def test_voledge_score_is_weighted_and_bounded():
    bars = load_ohlcv("UVIX")
    accuracy = calculate_historical_accuracy(bars, quality_threshold=0.004)
    pattern = detect_primary_pattern(bars, accuracy.historical_accuracy)
    score = score_opportunity(bars, accuracy, pattern, bars[-1].close, bars[-1].close - 2, bars[-1].close + 5)
    assert 0 <= score <= 100


def test_historical_accuracy_uses_matching_setups():
    stats = calculate_historical_accuracy(load_ohlcv("GLD"), quality_threshold=0.004)
    assert stats.matching_setups > 0
    assert 0 <= stats.historical_accuracy <= 100
    assert stats.best_holding_window == "5 trading days"


def test_historical_accuracy_can_score_bearish_direction():
    bearish_stats = calculate_historical_accuracy(load_ohlcv("SOXS"), quality_threshold=0.004, direction="Bearish")
    assert bearish_stats.matching_setups > 0
    assert 0 <= bearish_stats.historical_accuracy <= 100
    assert bearish_stats.expected_return > -100


def test_pattern_detection_returns_required_metrics():
    bars = load_ohlcv("SOXL")
    stats = calculate_historical_accuracy(bars, quality_threshold=0.004)
    pattern = detect_primary_pattern(bars, stats.historical_accuracy)
    assert pattern.name
    assert 0 <= pattern.quality_score <= 100
    assert pattern.confidence_level in {"Low", "Medium", "High"}


def test_intelligence_supports_sell_or_early_setup_language():
    candidates = [build_intelligence(symbol) for symbol in ("SOXS", "SQQQ", "LABD", "UVIX") if symbol in {"SOXS", "LABD", "UVIX"}]
    assert any(
        item.recommendation.value in {"Strong Sell", "Hedge Opportunity"} or "early setup" in item.ai_explanation
        for item in candidates
    )


def test_bearish_risk_reward_uses_absolute_distance():
    bars = load_ohlcv("SOXS")
    stats = calculate_historical_accuracy(bars, quality_threshold=0.004, direction="Bearish")
    pattern = detect_primary_pattern(bars, stats.historical_accuracy)
    score = score_opportunity(bars, stats, pattern, 50, 55, 40)
    assert 0 <= score <= 100


def test_sector_volatility_radar_is_ranked():
    sectors = sector_radar()
    assert len(sectors) >= 5
    assert sectors[0].sector_volatility_score >= sectors[-1].sector_volatility_score
    assert any(sector.symbol in {"IBIT", "ETHA"} for sector in sectors)


def test_crypto_etfs_are_supported_in_intelligence_and_radar():
    bitcoin = build_intelligence("IBIT")
    ethereum = build_intelligence("ETHA")
    radar_symbols = {item.symbol for item in opportunity_radar()}
    assert bitcoin.category == "Crypto Bitcoin"
    assert ethereum.category == "Crypto Ethereum"
    assert {"IBIT", "ETHA"}.issubset(radar_symbols)


def test_opportunity_radar_skips_failed_symbols(monkeypatch):
    from apps.api.app import services

    original = services.build_intelligence

    def flaky_build(symbol: str):
        if symbol == "SPY":
            raise RuntimeError("provider hiccup")
        return original(symbol)

    monkeypatch.setattr(services, "build_intelligence", flaky_build)
    radar = opportunity_radar()
    assert radar
    assert radar[0].vol_edge_score >= radar[-1].vol_edge_score


def test_alert_generation_evaluates_score_condition():
    result = evaluate_alert(Alert(id="test", symbol="UVIX", condition="VolEdge Score above", threshold=10))
    assert result.triggered is True
    assert result.vol_edge_score >= 0


def test_backtesting_returns_summary():
    result = run_signal_backtest(build_intelligence("GLD"))
    assert result.trades > 0
    assert result.best_window


def test_portfolio_risk_reports_dominant_exposure():
    report = build_portfolio_risk(["UVIX", "SOXL", "GLD"])
    assert report.risk_score > 0
    assert report.exposures


def test_live_provider_requires_api_key():
    for provider in (PolygonMarketDataProvider, TwelveDataMarketDataProvider, FinnhubMarketDataProvider):
        try:
            provider("")
        except ProviderNotConfiguredError:
            continue
        raise AssertionError(f"{provider.__name__} should require an API key")


def test_in_memory_store_persists_alert_and_watchlist_symbol():
    store = InMemoryStore()
    saved = store.create_alert(Alert(id="local", symbol="GLD", condition="Score above", threshold=75))
    assert saved in store.list_alerts()
    assert "SLV" in store.add_watchlist_symbol("SLV")
