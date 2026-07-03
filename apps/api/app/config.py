from __future__ import annotations

import os
from functools import lru_cache


class Settings:
    def __init__(self) -> None:
        self.app_name = os.getenv("APP_NAME", "VolEdge AI API")
        self.app_version = os.getenv("APP_VERSION", "0.1.0")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.market_data_provider = os.getenv("MARKET_DATA_PROVIDER", "sample-provider-ready")
        self.polygon_api_key = os.getenv("POLYGON_API_KEY", "")
        self.twelve_data_api_key = os.getenv("TWELVE_DATA_API_KEY", "")
        self.finnhub_api_key = os.getenv("FINNHUB_API_KEY", "")
        self.store_backend = os.getenv("STORE_BACKEND", "memory")
        self.supabase_url = os.getenv("SUPABASE_URL", "").rstrip("/")
        self.supabase_service_role_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")
        self.trading_enabled = os.getenv("TRADING_ENABLED", "false").lower() == "true"
        self.cors_origins = _parse_csv(
            os.getenv(
                "CORS_ORIGINS",
                "http://localhost:3000,http://127.0.0.1:3000",
            )
        )


def _parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
