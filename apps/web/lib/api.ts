import {
  alerts as fallbackAlerts,
  backtestRows as fallbackBacktestRows,
  opportunities as fallbackOpportunities,
  patternSignals as fallbackPatternSignals,
  riskExposures as fallbackRiskExposures,
  sectors as fallbackSectors,
  type Opportunity,
  type PatternInsight
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
  pattern: {
    name: string;
    direction: "Bullish" | "Bearish" | "Neutral";
    quality_score?: number;
    historical_accuracy?: number;
    confidence_level?: "Low" | "Medium" | "High";
    chart_score?: number;
    prediction_score?: number;
    breakout_probability?: number;
    breakdown_probability?: number;
    predicted_move?: string;
    key_level?: number | null;
    chart_summary?: string;
    evidence?: string[];
  };
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
  swing_transition?: {
    action: "Hold" | "Hold -> Buy" | "Hold -> Sell";
    status: "Waiting" | "Arming" | "Triggered" | "Invalidated";
    transition_score: number;
    trigger_price: number;
    trigger_gap_percent: number;
    reason: string;
  };
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

export type AccuracyInsight = {
  rank: number;
  symbol: string;
  category: string;
  action: Opportunity["action"];
  recommendation: Opportunity["recommendation"];
  qualifiedAccuracy: number;
  rawWinRate: number;
  matches: number;
  expectedValue: string;
  averageReturn: string;
  averageLoss: string;
  maxDrawdown: string;
  profitFactor: string;
  confidence: "Low" | "Medium" | "High";
  bestWindow: string;
  pattern: string;
  riskReward: string;
  gateStatus: "Trade Ready" | "Watch";
  explanation: string;
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
    transitionAction: item.swing_transition?.action ?? "Hold",
    transitionStatus: item.swing_transition?.status ?? "Waiting",
    transitionScore: Math.round(item.swing_transition?.transition_score ?? 0),
    transitionTrigger: item.swing_transition ? formatPrice(item.swing_transition.trigger_price) : item.suggested_entry.toFixed(2),
    triggerGap: `${(item.swing_transition?.trigger_gap_percent ?? 0).toFixed(1)}%`,
    transitionReason: item.swing_transition?.reason ?? "No directional transition is active yet.",
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

export async function getAccuracyData(): Promise<{ top: AccuracyInsight; rows: AccuracyInsight[]; usingFallback: boolean }> {
  const data = await apiGet<{ opportunities: ApiIntelligence[] }>("/api/radar");
  if (!data) {
    const rows: AccuracyInsight[] = fallbackOpportunities.map((item, index) => ({
      rank: index + 1,
      symbol: item.symbol,
      category: item.category,
      action: item.action,
      recommendation: item.recommendation,
      qualifiedAccuracy: item.accuracy,
      rawWinRate: item.rawWinRate ?? item.accuracy,
      matches: item.matches,
      expectedValue: item.expectedValue ?? item.expectedReturn,
      averageReturn: item.expectedReturn,
      averageLoss: item.averageLoss ?? "N/A",
      maxDrawdown: item.maxDrawdown ?? "N/A",
      profitFactor: item.profitFactor ?? "1.00",
      confidence: item.sampleConfidence ?? (item.confidence === "Very High" ? "High" : item.confidence),
      bestWindow: item.window,
      pattern: item.pattern,
      riskReward: item.riskReward,
      gateStatus: (item.action === "Watch" ? "Watch" : "Trade Ready") as AccuracyInsight["gateStatus"],
      explanation: item.explanation
    }));
    return { top: rows[0], rows, usingFallback: true };
  }

  const rows: AccuracyInsight[] = data.opportunities
    .map((item, index) => {
      const opportunity = mapOpportunity(item, index + 1);
      const evidence = item.evidence;
      return {
        rank: index + 1,
        symbol: item.symbol,
        category: item.category,
        action: opportunity.action,
        recommendation: item.recommendation,
        qualifiedAccuracy: Math.round(item.historical_accuracy),
        rawWinRate: Math.round(evidence?.historical_win_rate ?? item.historical_accuracy),
        matches: evidence?.sample_size ?? item.historical_matches,
        expectedValue: formatPercent(evidence?.expected_value ?? item.expected_return),
        averageReturn: formatPercent(evidence?.average_return ?? item.expected_return),
        averageLoss: formatPercent(evidence?.average_loss ?? 0),
        maxDrawdown: formatPercent(-(Math.abs(evidence?.maximum_drawdown ?? 0))),
        profitFactor: `${(evidence?.profit_factor ?? 1).toFixed(2)}`,
        confidence: evidence?.statistical_confidence ?? (item.confidence_level === "Very High" ? "High" : item.confidence_level),
        bestWindow: evidence?.best_holding_period ?? item.best_holding_window,
        pattern: item.pattern.name,
        riskReward: `${item.risk_reward.toFixed(1)}:1`,
        gateStatus: (opportunity.action === "Watch" ? "Watch" : "Trade Ready") as AccuracyInsight["gateStatus"],
        explanation: item.ai_explanation
      };
    })
    .sort((a, b) => {
      const gateBoost = (b.gateStatus === "Trade Ready" ? 100 : 0) - (a.gateStatus === "Trade Ready" ? 100 : 0);
      return gateBoost || b.qualifiedAccuracy - a.qualifiedAccuracy || Number(b.profitFactor) - Number(a.profitFactor);
    });

  return { top: rows[0], rows, usingFallback: false };
}

export async function getPatternData(): Promise<{ patterns: PatternInsight[]; usingFallback: boolean }> {
  const data = await apiGet<{ opportunities: ApiIntelligence[] }>("/api/radar");
  if (!data) {
    return { patterns: fallbackPatternSignals as PatternInsight[], usingFallback: true };
  }

  const patterns = data.opportunities
    .map((item) => {
      const quality = Math.round(item.pattern.quality_score ?? item.vol_edge_score);
      const historicalAccuracy = Math.round(item.pattern.historical_accuracy ?? item.historical_accuracy);
      const predictionScore = Math.round(item.pattern.prediction_score ?? item.confidence_score ?? quality);
      const keyLevel = typeof item.pattern.key_level === "number" ? formatPrice(item.pattern.key_level) : formatPrice(item.suggested_entry);
      return {
        symbol: item.symbol,
        name: item.pattern.name,
        direction: item.pattern.direction,
        confidence: item.pattern.confidence_level ?? (item.confidence_level === "Very High" ? "High" : item.confidence_level),
        quality,
        historicalAccuracy,
        predictionScore,
        breakoutProbability: Math.round(item.pattern.breakout_probability ?? (item.pattern.direction === "Bullish" ? predictionScore : 100 - predictionScore)),
        breakdownProbability: Math.round(item.pattern.breakdown_probability ?? (item.pattern.direction === "Bearish" ? predictionScore : 100 - predictionScore)),
        predictedMove: item.pattern.predicted_move ?? (item.pattern.direction === "Bullish" ? "Bullish follow-through" : item.pattern.direction === "Bearish" ? "Bearish follow-through" : "Wait for range break"),
        keyLevel,
        currentPrice: formatPrice(item.latest_price ?? item.suggested_entry),
        evidence: item.pattern.evidence?.length ? item.pattern.evidence : ["pattern evidence pending"],
        summary: item.pattern.chart_summary ?? item.ai_explanation
      };
    })
    .sort((a, b) => b.predictionScore - a.predictionScore)
    .slice(0, 8);

  return { patterns, usingFallback: false };
}

export async function getBacktestData(symbol = "UVIX") {
  const data = await apiGet<{
    windows: Array<{
      window: string;
      trades: number;
      win_rate: number;
      raw_win_rate?: number;
      average_return: number;
      expected_return?: number;
      max_drawdown: number;
      profit_factor?: number;
      filter?: string;
    }>;
  }>(`/api/backtest/${symbol}`);
  if (!data) {
    return fallbackBacktestRows;
  }
  return data.windows.map((item) => ({
    window: item.window,
    trades: item.trades,
    winRate: `${item.win_rate.toFixed(0)}%`,
    rawWinRate: typeof item.raw_win_rate === "number" ? `${item.raw_win_rate.toFixed(0)}%` : "N/A",
    avgReturn: formatPercent(item.average_return),
    expectedReturn: typeof item.expected_return === "number" ? formatPercent(item.expected_return) : formatPercent(item.average_return),
    drawdown: `-${item.max_drawdown.toFixed(1)}%`,
    profitFactor: typeof item.profit_factor === "number" ? item.profit_factor.toFixed(2) : "API",
    filter: item.filter ?? "Qualified setup"
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
