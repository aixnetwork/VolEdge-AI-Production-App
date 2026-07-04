export type Opportunity = {
  rank: number;
  symbol: string;
  category: string;
  currentPrice: string;
  priceChange: string;
  priceChangePercent: string;
  priceTone: "mint" | "amber" | "white";
  priceSource: string;
  priceAsOf: string;
  score: number;
  confidenceScore?: number;
  riskScore?: number;
  accuracy: number;
  rawWinRate?: number;
  confidence: "Very High" | "High" | "Medium" | "Low";
  matches: number;
  expectedReturn: string;
  expectedValue?: string;
  averageLoss?: string;
  maxDrawdown?: string;
  profitFactor?: string;
  sampleConfidence?: "Low" | "Medium" | "High";
  window: string;
  marketRegime?: string;
  regimeEvidence?: string;
  timeframeAlignment?: number;
  institutionalScore?: number;
  adaptiveWeightSummary?: string;
  transitionAction?: "Hold" | "Hold -> Buy" | "Hold -> Sell";
  transitionStatus?: "Waiting" | "Arming" | "Triggered" | "Invalidated";
  transitionScore?: number;
  transitionTrigger?: string;
  triggerGap?: string;
  transitionReason?: string;
  recommendation: "Extreme Buy" | "Strong Buy" | "Watch" | "Strong Sell" | "Hedge Opportunity";
  action: "Buy" | "Sell" | "Watch";
  triggerSide: "High Trigger" | "Low Trigger" | "Range Trigger";
  pattern: string;
  entry: string;
  stop: string;
  target: string;
  riskReward: string;
  explanation: string;
};

export type PatternInsight = {
  symbol: string;
  name: string;
  direction: "Bullish" | "Bearish" | "Neutral";
  confidence: "High" | "Medium" | "Low";
  quality: number;
  historicalAccuracy: number;
  predictionScore: number;
  breakoutProbability: number;
  breakdownProbability: number;
  predictedMove: string;
  keyLevel: string;
  currentPrice: string;
  evidence: string[];
  summary: string;
};

export const opportunities: Opportunity[] = [
  {
    rank: 1,
    symbol: "UVIX",
    category: "Volatility",
    currentPrice: "14.52",
    priceChange: "+0.44",
    priceChangePercent: "+3.1%",
    priceTone: "mint",
    priceSource: "sample-provider-ready",
    priceAsOf: "Latest bar",
    score: 91,
    confidenceScore: 84,
    riskScore: 38,
    accuracy: 67,
    rawWinRate: 69,
    confidence: "Very High",
    matches: 84,
    expectedReturn: "+8.4%",
    expectedValue: "+5.6%",
    averageLoss: "-3.1%",
    maxDrawdown: "-4.2%",
    profitFactor: "1.82",
    sampleConfidence: "High",
    window: "3-5 trading days",
    marketRegime: "High Volatility",
    regimeEvidence: "SPY trend, QQQ trend, and volatility expansion support active volatility monitoring.",
    timeframeAlignment: 83,
    institutionalScore: 81,
    adaptiveWeightSummary: "historical accuracy, volatility expansion, trend alignment",
    transitionAction: "Hold -> Buy",
    transitionStatus: "Arming",
    transitionScore: 82,
    transitionTrigger: "14.80",
    triggerGap: "1.4%",
    transitionReason: "Hold until the buy trigger confirms. The setup is 1.4% from trigger with high historical accuracy.",
    recommendation: "Extreme Buy",
    action: "Buy",
    triggerSide: "High Trigger",
    pattern: "Volatility Expansion",
    entry: "14.80",
    stop: "13.45",
    target: "18.20",
    riskReward: "2.5:1",
    explanation:
      "UVIX ranks first because volatility expansion is accelerating while historical matching setups show the strongest short-window payoff profile."
  },
  {
    rank: 2,
    symbol: "SOXL",
    category: "Semiconductors",
    currentPrice: "62.42",
    priceChange: "+1.16",
    priceChangePercent: "+1.9%",
    priceTone: "mint",
    priceSource: "sample-provider-ready",
    priceAsOf: "Latest bar",
    score: 86,
    accuracy: 63,
    confidence: "High",
    matches: 76,
    expectedReturn: "+6.1%",
    window: "5 trading days",
    recommendation: "Strong Buy",
    action: "Buy",
    triggerSide: "High Trigger",
    pattern: "Breakout",
    entry: "62.10",
    stop: "58.20",
    target: "70.40",
    riskReward: "2.1:1",
    explanation: "Semiconductor momentum is confirming a breakout with strong volume participation."
  },
  {
    rank: 3,
    symbol: "GLD",
    category: "Gold",
    currentPrice: "219.72",
    priceChange: "+0.68",
    priceChangePercent: "+0.3%",
    priceTone: "mint",
    priceSource: "sample-provider-ready",
    priceAsOf: "Latest bar",
    score: 82,
    accuracy: 61,
    confidence: "High",
    matches: 92,
    expectedReturn: "+3.2%",
    window: "8 trading days",
    recommendation: "Strong Buy",
    action: "Buy",
    triggerSide: "High Trigger",
    pattern: "Ascending Triangle",
    entry: "219.40",
    stop: "214.60",
    target: "229.20",
    riskReward: "2.0:1",
    explanation: "Gold is showing constructive compression with stable historical follow-through."
  },
  {
    rank: 4,
    symbol: "XBI",
    category: "Biotech",
    currentPrice: "95.84",
    priceChange: "-0.38",
    priceChangePercent: "-0.4%",
    priceTone: "amber",
    priceSource: "sample-provider-ready",
    priceAsOf: "Latest bar",
    score: 77,
    accuracy: 58,
    confidence: "Medium",
    matches: 69,
    expectedReturn: "+4.7%",
    window: "6 trading days",
    recommendation: "Watch",
    action: "Watch",
    triggerSide: "Range Trigger",
    pattern: "Bull Flag",
    entry: "96.30",
    stop: "91.75",
    target: "104.80",
    riskReward: "1.9:1",
    explanation: "Biotech is improving, though confirmation is still less decisive than the top-ranked opportunities."
  },
  {
    rank: 5,
    symbol: "IBIT",
    category: "Crypto Bitcoin",
    currentPrice: "67.12",
    priceChange: "+1.02",
    priceChangePercent: "+1.5%",
    priceTone: "mint",
    priceSource: "sample-provider-ready",
    priceAsOf: "Latest bar",
    score: 75,
    accuracy: 59,
    confidence: "Medium",
    matches: 58,
    expectedReturn: "+5.8%",
    window: "5 trading days",
    recommendation: "Strong Buy",
    action: "Buy",
    triggerSide: "High Trigger",
    pattern: "Pre-Breakout Compression",
    entry: "67.40",
    stop: "63.10",
    target: "76.20",
    riskReward: "2.0:1",
    explanation: "Bitcoin exposure is compressing near resistance with improving volume confirmation."
  },
  {
    rank: 6,
    symbol: "ETHA",
    category: "Crypto Ethereum",
    currentPrice: "31.44",
    priceChange: "-0.18",
    priceChangePercent: "-0.6%",
    priceTone: "amber",
    priceSource: "sample-provider-ready",
    priceAsOf: "Latest bar",
    score: 72,
    accuracy: 57,
    confidence: "Medium",
    matches: 47,
    expectedReturn: "+4.9%",
    window: "5 trading days",
    recommendation: "Watch",
    action: "Watch",
    triggerSide: "Range Trigger",
    pattern: "Volatility Expansion",
    entry: "31.80",
    stop: "29.60",
    target: "36.20",
    riskReward: "2.0:1",
    explanation: "Ethereum exposure is active, but the model waits for cleaner trend alignment before upgrading it."
  }
];

export const sectors = [
  { sector: "Volatility", symbol: "UVIX", score: 94, signal: "Extreme Buy", strength: "+18.2%" },
  { sector: "Semiconductors", symbol: "SOXX", score: 88, signal: "Strong Buy", strength: "+7.4%" },
  { sector: "Crypto Bitcoin", symbol: "IBIT", score: 82, signal: "Strong Buy", strength: "+6.8%" },
  { sector: "Crypto Ethereum", symbol: "ETHA", score: 73, signal: "Watch", strength: "+3.9%" },
  { sector: "Gold Miners", symbol: "GDX", score: 80, signal: "Strong Buy", strength: "+5.2%" },
  { sector: "Energy", symbol: "XLE", score: 54, signal: "Watch", strength: "+1.1%" }
];

export const accuracyBreakdown = [
  { label: "Historical Win Rate", value: "67%", detail: "84 matching setups" },
  { label: "Average Return", value: "+8.4%", detail: "Best 3-5 day window" },
  { label: "Average Drawdown", value: "-3.1%", detail: "Measured from OHLCV ranges" },
  { label: "Profit Factor", value: "1.82", detail: "Gross gains over losses" },
  { label: "Expected Return", value: "+5.6%", detail: "Win-rate adjusted" },
  { label: "Confidence Level", value: "High", detail: "Enough historical matches" }
];

export const patternSignals = [
  {
    symbol: "UVIX",
    name: "Volatility Expansion",
    quality: 91,
    historicalAccuracy: 67,
    predictionScore: 84,
    breakoutProbability: 84,
    breakdownProbability: 8,
    keyLevel: "14.80",
    currentPrice: "14.52",
    predictedMove: "Buy trigger forming",
    confidence: "High",
    direction: "Bullish",
    evidence: ["relative volume 1.28x", "multi-timeframe alignment 83/100", "institutional confirmation 81/100"],
    summary: "Volatility Expansion has an 84/100 AI chart score with resistance near 14.80."
  },
  {
    symbol: "SOXL",
    name: "Gap Breakout",
    quality: 84,
    historicalAccuracy: 62,
    predictionScore: 78,
    breakoutProbability: 78,
    breakdownProbability: 14,
    keyLevel: "62.10",
    currentPrice: "62.42",
    predictedMove: "Bullish follow-through",
    confidence: "Medium",
    direction: "Bullish",
    evidence: ["price closed above resistance", "relative volume 1.16x", "trend alignment positive"],
    summary: "Gap Breakout has a 78/100 AI chart score with resistance near 62.10."
  },
  {
    symbol: "IBIT",
    name: "Pre-Breakout Compression",
    quality: 79,
    historicalAccuracy: 59,
    predictionScore: 76,
    breakoutProbability: 76,
    breakdownProbability: 16,
    keyLevel: "67.40",
    currentPrice: "67.12",
    predictedMove: "Buy trigger forming",
    confidence: "Medium",
    direction: "Bullish",
    evidence: ["tight range compression", "rising lows", "crypto ETF trend support"],
    summary: "Pre-Breakout Compression has a 76/100 AI chart score with resistance near 67.40."
  }
];

export const backtestRows = [
  { window: "3 days", trades: 84, winRate: "64%", rawWinRate: "69%", avgReturn: "+4.1%", expectedReturn: "+2.6%", drawdown: "-2.2%", profitFactor: "1.54", filter: "Qualified setup only" },
  { window: "5 days", trades: 84, winRate: "67%", rawWinRate: "72%", avgReturn: "+8.4%", expectedReturn: "+5.6%", drawdown: "-3.1%", profitFactor: "1.82", filter: "Qualified setup only" },
  { window: "8 days", trades: 79, winRate: "61%", rawWinRate: "66%", avgReturn: "+7.2%", expectedReturn: "+4.4%", drawdown: "-4.6%", profitFactor: "1.39", filter: "Qualified setup only" }
];

export const alerts = [
  { symbol: "UVIX", condition: "VolEdge Score above 85", status: "Armed" },
  { symbol: "SOXL", condition: "Breakout confirmed by volume", status: "Watching" },
  { symbol: "IBIT", condition: "Crypto ETF high trigger confirmed", status: "Armed" },
  { symbol: "GLD", condition: "Accuracy above 60%", status: "Armed" }
];

export const riskExposures = [
  { label: "Volatility Long", value: "42%", tone: "High" },
  { label: "Semiconductor Beta", value: "28%", tone: "Elevated" },
  { label: "Precious Metals", value: "18%", tone: "Balanced" },
  { label: "Cash Buffer", value: "12%", tone: "Available" }
];

export const productArchitecture = [
  "Opportunity Radar",
  "Sector Volatility Radar",
  "Pattern Recognition AI",
  "Historical Accuracy Engine",
  "ETF Intelligence",
  "Gold & Silver Intelligence",
  "Crypto ETF Intelligence",
  "Volatility Intelligence",
  "Portfolio Intelligence",
  "Alert Center"
];

export const referenceTaglines = {
  primary: "Where Volatility Becomes Opportunity",
  alternate: "Find the Edge. Trade with Confidence."
};
