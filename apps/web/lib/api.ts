import {
  alerts as fallbackAlerts,
  backtestRows as fallbackBacktestRows,
  opportunities as fallbackOpportunities,
  riskExposures as fallbackRiskExposures,
  sectors as fallbackSectors,
  type Opportunity
} from "@/lib/mock-data";

const apiBaseUrl = process.env.NEXT_PUBLIC_API_BASE_URL;

type ApiIntelligence = {
  symbol: string;
  category: string;
  vol_edge_score: number;
  historical_accuracy: number;
  confidence_level: Opportunity["confidence"];
  historical_matches: number;
  expected_return: number;
  best_holding_window: string;
  recommendation: Opportunity["recommendation"];
  pattern: { name: string };
  suggested_entry: number;
  suggested_stop_loss: number;
  suggested_target: number;
  risk_reward: number;
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

function mapOpportunity(item: ApiIntelligence, rank: number): Opportunity {
  return {
    rank,
    symbol: item.symbol,
    category: item.category,
    score: Math.round(item.vol_edge_score),
    accuracy: Math.round(item.historical_accuracy),
    confidence: item.confidence_level,
    matches: item.historical_matches,
    expectedReturn: formatPercent(item.expected_return),
    window: item.best_holding_window,
    recommendation: item.recommendation,
    pattern: item.pattern.name,
    entry: item.suggested_entry.toFixed(2),
    stop: item.suggested_stop_loss.toFixed(2),
    target: item.suggested_target.toFixed(2),
    riskReward: `${item.risk_reward.toFixed(1)}:1`,
    explanation: item.ai_explanation
  };
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
