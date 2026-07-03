import {
  alerts as fallbackAlerts,
  backtestRows as fallbackBacktestRows,
  opportunities as fallbackOpportunities,
  riskExposures as fallbackRiskExposures,
  sectors as fallbackSectors,
  type Opportunity
} from "@/lib/mock-data";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL ?? "https://voledge-ai-api.onrender.com";

type ApiIntelligence = {
  symbol: string;
  category: string;
  latest_price?: number;
  price_change?: number | null;
  price_change_percent?: number | null;
  price_timestamp?: string;
  price_provider?: string;
  price_realtime?: boolean;
  vol_edge_score: number;
  confidence_score?: number;
  risk_score?: number;
  historical_accuracy: number;
  confidence_level: Opportunity["confidence"];
  historical_matches: number;
  expected_return: number;
  best_holding_window: string;
  recommendation: Opportunity["recommendation"];
  pattern: { name: string; direction: "Bullish" | "Bearish" | "Neutral" };
  suggested_entry: number;
  suggested_stop_loss: number;
  suggested_target: number;
  risk_reward: number;
  market_regime?: { name: string; evidence: string };
  evidence?: {
    historical_win_rate: number;
    historical_accuracy: number;
    sample_size: number;
    statistical_confidence: "Low" | "Medium" | "High";
    average_return: number;
    average_loss: number;
    maximum_drawdown: number;
    profit_factor: number;
    expected_value: number;
    best_holding_period: string;
  };
  timeframe_confirmation?: { alignment_score: number };
  institutional_confirmation?: { confirmation_score: number };
  adaptive_weights?: Record<string, number>;
  ai_explanation: string;
};

type ApiSector = {
  sector: string;
  symbol: string;
  sector_volatility_score: number;
  recommendation: string;
  relative_strength_vs_spy: number;
};

async function apiGet<T>(path: string): Promise<T | null> {
  if (!apiBaseUrl) {
    return null;
  }

  try {
    const response = await fetch(`${apiBaseUrl}${path}`, {
      cache: "no-store",
      headers: { Accept: "application/json" }
    });
    if (!response.ok) {
      return null;
    }
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

function formatPercent(value: number): string {
  const sign = value > 0 ? "+" : "";
  return `${sign}${value.toFixed(1)}%`;
}

function formatPrice(value: number): string {
  return value.toFixed(value >= 100 ? 2 : 4).replace(/0+$/, "").replace(/\.$/, "");
}

function mapOpportunity(item: ApiIntelligence, rank: number): Opportunity {
  const action: Opportunity["action"] =
    item.recommendation === "Strong Sell" || item.recommendation === "Hedge Opportunity"
      ? "Sell"
      : item.recommendation === "Extreme Buy" || item.recommendation === "Strong Buy"
      ? "Buy"
      : "Watch";
  const triggerSide: Opportunity["triggerSide"] =
    action === "Sell" ? "Low Trigger" : action === "Buy" ? "High Trigger" : "Range Trigger";
  const hasPrice = typeof item.latest_price === "number" && Number.isFinite(item.latest_price);
  const price = hasPrice ? item.latest_price as number : item.suggested_entry;
  const priceSource = hasPrice
    ? item.price_realtime
      ? `${item.price_provider ?? "market"} live`
      : `${item.price_provider ?? "market"} delayed`
    : "API price pending";

  return {
    rank,
    symbol: item.symbol,
    category: item.category,
    currentPrice: formatPrice(price),
    priceChange: typeof item.price_change === "number" ? `${item.price_change > 0 ? "+" : ""}${formatPrice(item.price_change)}` : "N/A",
    priceChangePercent: typeof item.price_change_percent === "number" ? formatPercent(item.price_change_percent) : "N/A",
    priceTone: typeof item.price_change_percent !== "number" ? "white" : item.price_change_percent >= 0 ? "mint" : "amber",
    priceSource,
    priceAsOf: item.price_timestamp ?? "Pending API redeploy",
    score: Math.round(item.vol_edge_score),
    confidenceScore: Math.round(item.confidence_score ?? item.historical_accuracy),
    riskScore: Math.round(item.risk_score ?? 50),
    accuracy: Math.round(item.historical_accuracy),
    rawWinRate: Math.round(item.evidence?.historical_win_rate ?? item.historical_accuracy),
    confidence: item.confidence_level,
    matches: item.evidence?.sample_size ?? item.historical_matches,
    expectedReturn: formatPercent(item.evidence?.average_return ?? item.expected_return),
    expectedValue: formatPercent(item.evidence?.expected_value ?? item.expected_return),
    averageLoss: formatPercent(item.evidence?.average_loss ?? 0),
    maxDrawdown: formatPercent(-(Math.abs(item.evidence?.maximum_drawdown ?? 0))),
    profitFactor: `${(item.evidence?.profit_factor ?? 1).toFixed(2)}`,
    sampleConfidence: item.evidence?.statistical_confidence ?? (item.confidence_level === "Very High" ? "High" : item.confidence_level),
    window: item.evidence?.best_holding_period ?? item.best_holding_window,
    marketRegime: item.market_regime?.name ?? "Pending regime",
    regimeEvidence: item.market_regime?.evidence ?? "",
    timeframeAlignment: Math.round(item.timeframe_confirmation?.alignment_score ?? 0),
    institutionalScore: Math.round(item.institutional_confirmation?.confirmation_score ?? 0),
    adaptiveWeightSummary: summarizeWeights(item.adaptive_weights),
    recommendation: item.recommendation,
    action,
    triggerSide,
    pattern: item.pattern.name,
    entry: item.suggested_entry.toFixed(2),
    stop: item.suggested_stop_loss.toFixed(2),
    target: item.suggested_target.toFixed(2),
    riskReward: `${item.risk_reward.toFixed(1)}:1`,
    explanation: item.ai_explanation
  };
}

function summarizeWeights(weights?: Record<string, number>): string {
  if (!weights) {
    return "adaptive weights pending";
  }
  const labels: Record<string, string> = {
    accuracy: "historical accuracy",
    pattern: "pattern reliability",
    volatility: "volatility expansion",
    momentum: "momentum",
    risk_reward: "risk/reward",
    volume: "relative volume",
    trend: "trend alignment",
    timeframe: "multi-timeframe alignment",
    institutional: "institutional confirmation"
  };
  return Object.entries(weights)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 3)
    .map(([name]) => labels[name] ?? name)
    .join(", ");
}

export async function getRadarData() {
  const data = await apiGet<{ top_opportunity: ApiIntelligence; opportunities: ApiIntelligence[] }>("/api/radar");
  if (!data) {
    return { top: fallbackOpportunities[0], opportunities: fallbackOpportunities, usingFallback: true };
  }

  const opportunities = data.opportunities.map((item, index) => mapOpportunity(item, index + 1));
  return {
    top: mapOpportunity(data.top_opportunity, 1),
    opportunities,
    usingFallback: false
  };
}

export async function getOpportunity(symbol: string) {
  const data = await apiGet<ApiIntelligence>(`/api/intelligence/${symbol}`);
  if (!data) {
    return fallbackOpportunities.find((item) => item.symbol === symbol.toUpperCase()) ?? fallbackOpportunities[0];
  }
  return mapOpportunity(data, 1);
}

export async function getSectorData() {
  const data = await apiGet<{ sectors: ApiSector[] }>("/api/sectors/radar");
  if (!data) {
    return fallbackSectors;
  }
  return data.sectors.map((item) => ({
    sector: item.sector,
    symbol: item.symbol,
    score: Math.round(item.sector_volatility_score),
    signal: item.recommendation,
    strength: formatPercent((item.relative_strength_vs_spy - 50) / 10)
  }));
}

export async function getBacktestData(symbol = "UVIX") {
  const data = await apiGet<{
    windows: Array<{ window: string; trades: number; win_rate: number; average_return: number; max_drawdown: number }>;
  }>(`/api/backtest/${symbol}`);
  if (!data) {
    return fallbackBacktestRows;
  }
  return data.windows.map((item) => ({
    window: item.window,
    trades: item.trades,
    winRate: `${item.win_rate.toFixed(0)}%`,
    avgReturn: formatPercent(item.average_return),
    drawdown: `-${item.max_drawdown.toFixed(1)}%`,
    profitFactor: "API"
  }));
}

export async function getAlertsData() {
  const data = await apiGet<{ alerts: Array<{ symbol: string; condition: string }>; evaluations: Array<{ symbol: string; triggered: boolean }> }>("/api/alerts");
  if (!data) {
    return fallbackAlerts;
  }
  return data.alerts.map((alert) => {
    const evaluation = data.evaluations.find((item) => item.symbol === alert.symbol);
    return {
      symbol: alert.symbol,
      condition: alert.condition,
      status: evaluation?.triggered ? "Triggered" : "Armed"
    };
  });
}

export async function getRiskData() {
  const data = await apiGet<{ exposures: Array<{ label: string; value: number; status: string }> }>("/api/risk");
  if (!data) {
    return fallbackRiskExposures;
  }
  return data.exposures.map((item) => ({
    label: item.label,
    value: `${item.value.toFixed(0)}%`,
    tone: item.status
  }));
}
