from fastapi.testclient import TestClient

from apps.api.app.main import app


client = TestClient(app)


def test_radar_endpoint_returns_top_opportunity():
    response = client.get("/api/radar")
    assert response.status_code == 200
    body = response.json()
    assert body["top_opportunity"]["vol_edge_score"] >= body["opportunities"][-1]["vol_edge_score"]


def test_cache_warm_endpoint_primes_radar_cache():
    response = client.get("/api/cache/warm")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "warm"
    assert body["symbols"] > 0
    assert body["sector_symbols"] > 0
    assert body["cache_ttl_seconds"] >= 60


def test_intelligence_endpoint_includes_manual_approval():
    response = client.get("/api/intelligence/UVIX")
    assert response.status_code == 200
    body = response.json()
    assert body["manual_approval_required"] is True
    assert body["latest_price"] > 0
    assert body["price_provider"]
    assert "price_change_percent" in body
    assert 0 <= body["confidence_score"] <= 100
    assert 0 <= body["risk_score"] <= 100
    assert body["market_regime"]["name"]
    assert body["evidence"]["sample_size"] > 0
    assert body["timeframe_confirmation"]["alignment_score"] >= 0
    assert body["institutional_confirmation"]["confirmation_score"] >= 0
    assert 0 <= body["pattern"]["chart_score"] <= 100
    assert 0 <= body["pattern"]["prediction_score"] <= 100
    assert 0 <= body["pattern"]["breakout_probability"] <= 100
    assert 0 <= body["pattern"]["breakdown_probability"] <= 100
    assert body["pattern"]["predicted_move"]
    assert body["pattern"]["chart_summary"]
    assert body["pattern"]["evidence"]
    assert body["swing_transition"]["action"] in {"Hold", "Hold -> Buy", "Hold -> Sell"}
    assert 0 <= body["swing_transition"]["transition_score"] <= 100
    assert body["swing_transition"]["trigger_price"] > 0
    assert body["confidence_level"] in {"Low", "Medium", "High", "Very High"}
    if body["pattern"]["direction"] == "Bearish":
        assert body["suggested_stop_loss"] > body["suggested_entry"]
        assert body["suggested_target"] < body["suggested_entry"]
    else:
        assert body["suggested_entry"] > body["suggested_stop_loss"]
        assert body["suggested_target"] > body["suggested_entry"]


def test_market_quote_endpoint_returns_provider_status():
    response = client.get("/api/market/quote/UVIX")
    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "UVIX"
    assert body["price"] > 0
    assert body["provider"] == "sample-provider-ready"
    assert body["realtime"] is False


def test_market_history_endpoint_caps_and_returns_bars():
    response = client.get("/api/market/history/UVIX?bars=5")
    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "UVIX"
    assert len(body["bars"]) == 5
    assert body["bars"][-1]["close"] > 0


def test_crypto_etf_intelligence_endpoint():
    response = client.get("/api/intelligence/IBIT")
    assert response.status_code == 200
    body = response.json()
    assert body["symbol"] == "IBIT"
    assert body["category"] == "Crypto Bitcoin"


def test_alert_generation():
    response = client.post("/api/alerts", json={"symbol": "GLD", "condition": "Score above", "threshold": 75})
    assert response.status_code == 200
    assert response.json()["active"] is True


def test_backtest_endpoint_returns_expected_fields():
    response = client.get("/api/backtest/GLD")
    assert response.status_code == 200
    body = response.json()
    assert body["summary"]["trades"] > 0
    assert body["summary"]["profit_factor"] >= 1
    assert len(body["windows"]) == 3
    assert body["windows"][0]["filter"] == "Qualified setup only"
    assert body["windows"][0]["profit_factor"] >= 1
