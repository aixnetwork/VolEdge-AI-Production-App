from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class Recommendation(str, Enum):
    EXTREME_BUY = "Extreme Buy"
    STRONG_BUY = "Strong Buy"
    WATCH = "Watch"
    STRONG_SELL = "Strong Sell"
    HEDGE = "Hedge Opportunity"


@dataclass(frozen=True)
class OhlcvBar:
    date: str
    open: float
    high: float
    low: float
    close: float
    volume: int


class MarketQuote(BaseModel):
    symbol: str
    price: float
    previous_close: float | None = None
    change: float | None = None
    change_percent: float | None = None
    bid: float | None = None
    ask: float | None = None
    volume: int | None = None
    timestamp: str
    provider: str
    realtime: bool


class AccuracyStats(BaseModel):
    historical_win_rate: float
    historical_accuracy: float
    matching_setups: int
    average_return: float
    average_drawdown: float
    profit_factor: float
    expected_return: float
    best_holding_window: str
    confidence_level: Literal["Low", "Medium", "High"]


class MarketRegime(BaseModel):
    name: Literal[
        "Bull Market",
        "Bear Market",
        "Sideways Market",
        "High Volatility",
        "Low Volatility",
        "Risk-On",
        "Risk-Off",
        "Crisis Mode",
    ]
    risk_bias: Literal["Risk-On", "Risk-Off", "Neutral"]
    volatility_state: Literal["Low", "Normal", "High"]
    confidence_modifier: float
    evidence: str


class MultiTimeframeConfirmation(BaseModel):
    weekly_trend: Literal["Aligned", "Mixed", "Against"]
    daily_trend: Literal["Aligned", "Mixed", "Against"]
    four_hour_trend: Literal["Aligned", "Mixed", "Against"]
    alignment_score: float = Field(ge=0, le=100)


class InstitutionalConfirmation(BaseModel):
    relative_volume: float
    atr_expansion: float
    relative_strength_vs_benchmark: float
    sector_rotation: float = Field(ge=0, le=100)
    trend_strength: float = Field(ge=0, le=100)
    ema_alignment: float = Field(ge=0, le=100)
    bollinger_expansion: float = Field(ge=0, le=100)
    confirmation_score: float = Field(ge=0, le=100)


class EvidenceReport(BaseModel):
    historical_win_rate: float
    historical_accuracy: float
    sample_size: int
    statistical_confidence: Literal["Low", "Medium", "High"]
    average_return: float
    average_loss: float
    maximum_drawdown: float
    profit_factor: float
    expected_value: float
    best_holding_period: str


class PatternSignal(BaseModel):
    name: str
    quality_score: float = Field(ge=0, le=100)
    historical_accuracy: float = Field(ge=0, le=100)
    confidence_level: Literal["Low", "Medium", "High"]
    direction: Literal["Bullish", "Bearish", "Neutral"]


class Intelligence(BaseModel):
    symbol: str
    category: str
    latest_price: float
    price_change: float | None = None
    price_change_percent: float | None = None
    price_timestamp: str
    price_provider: str
    price_realtime: bool
    vol_edge_score: float = Field(ge=0, le=100)
    confidence_score: float = Field(ge=0, le=100)
    risk_score: float = Field(ge=0, le=100)
    historical_accuracy: float = Field(ge=0, le=100)
    confidence_level: Literal["Low", "Medium", "High", "Very High"]
    historical_matches: int
    expected_return: float
    best_holding_window: str
    recommendation: Recommendation
    pattern: PatternSignal
    suggested_entry: float
    suggested_stop_loss: float
    suggested_target: float
    risk_reward: float
    market_regime: MarketRegime
    evidence: EvidenceReport
    timeframe_confirmation: MultiTimeframeConfirmation
    institutional_confirmation: InstitutionalConfirmation
    adaptive_weights: dict[str, float]
    ai_explanation: str
    manual_approval_required: bool = True


class SectorSignal(BaseModel):
    sector: str
    symbol: str
    sector_volatility_score: float = Field(ge=0, le=100)
    recommendation: Recommendation
    atr_expansion: float
    realized_volatility_spike: float
    volume_surge: float
    relative_strength_vs_spy: float


class AlertCreate(BaseModel):
    symbol: str
    condition: str
    threshold: float


class Alert(AlertCreate):
    id: str
    active: bool = True


class WatchlistAdd(BaseModel):
    symbol: str


class BacktestResult(BaseModel):
    symbol: str
    strategy: str
    trades: int
    win_rate: float
    expected_return: float
    max_drawdown: float
    profit_factor: float
    best_window: str


class AlertEvaluation(BaseModel):
    symbol: str
    triggered: bool
    reason: str
    vol_edge_score: float


class RiskExposure(BaseModel):
    label: str
    value: float
    status: Literal["Balanced", "Elevated", "High", "Available"]


class PortfolioRiskReport(BaseModel):
    risk_score: float = Field(ge=0, le=100)
    dominant_exposure: str
    correlation_watch: str
    exposures: list[RiskExposure]
    guardrails: list[str]
