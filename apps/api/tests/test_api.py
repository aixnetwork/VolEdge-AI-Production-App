from fastapi.testclient import TestClient

from apps.api.app.main import app


client = TestClient(app)


def test_radar_endpoint_returns_top_opportunity():
    response = client.get("/api/radar")
    assert response.status_code == 200
    body = response.json()
    assert body["top_opportunity"]["vol_edge_score"] >= body["opportunities"][-1]["vol_edge_score"]


def test_intelligence_endpoint_includes_manual_approval():
    response = client.get("/api/intelligence/UVIX")
    assert response.status_code == 200
    body = response.json()
    assert body["manual_approval_required"] is True
    assert body["confidence_level"] in {"Low", "Medium", "High", "Very High"}
    assert body["suggested_entry"] > body["suggested_stop_loss"]
    assert body["suggested_target"] > body["suggested_entry"]


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
