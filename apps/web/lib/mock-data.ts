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
    currentPrice: "61.96",
    priceChange: "-0.52",
    priceChangePercent: "-0.8%",
    priceTone: "amber",
    priceSource: "yfinance delayed fallback",
    priceAsOf: "2026-07-02 close",
    score: 64,
    confidenceScore: 58,
    riskScore: 72,
    accuracy: 58,
    rawWinRate: 59,
    confidence: "Medium",
    matches: 32,
    expectedReturn: "-1.2%",
    expectedValue: "-0.7%",
    averageLoss: "-3.4%",
    maxDrawdown: "-6.2%",
    profitFactor: "1.08",
    sampleConfidence: "Medium",
    window: "5 trading days",
    marketRegime: "High Volatility",
    regimeEvidence: "SPY trend, QQQ trend, and volatility expansion support active volatility monitoring.",
    timeframeAlignment: 83,
    institutionalScore: 81,
    adaptiveWeightSummary: "historical accuracy, volatility expansion, trend alignment",
    transitionAction: "Hold -> Sell",
    transitionStatus: "Waiting",
    transitionScore: 58,
    transitionTrigger: "59.90",
    triggerGap: "3.3%",
    transitionReason: "Hold until a sell trigger confirms. The fallback setup is based on delayed adjusted data while live API data is unavailable.",
    recommendation: "Watch",
    action: "Watch",
    triggerSide: "Range Trigger",
    pattern: "Historical Bearish Analog",
    entry: "59.90",
    stop: "64.60",
    target: "52.20",
    riskReward: "1.6:1",
    explanation:
      "UVIX fallback pricing is split-adjusted near 61.96. Live API data should be used before acting on any volatility ETF signal."
  },
  {
    rank: 2,
    symbol: "SOXL",
    category: "Semiconductors",
    currentPrice: "181.47",
    priceChange: "-36.08",
    priceChangePercent: "-16.6%",
    priceTone: "amber",
    priceSource: "yfinance delayed fallback",
    priceAsOf: "2026-07-02 close",
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
    entry: "184.00",
    stop: "169.50",
    target: "213.00",
    riskReward: "2.1:1",
    explanation: "Semiconductor momentum is confirming a breakout with strong volume participation."
  },
  {
    rank: 3,
    symbol: "GLD",
    category: "Gold",
    currentPrice: "378.13",
    priceChange: "+7.53",
    priceChangePercent: "+2.0%",
    priceTone: "mint",
    priceSource: "yfinance delayed fallback",
    priceAsOf: "2026-07-02 close",
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
    entry: "379.20",
    stop: "366.40",
    target: "404.80",
    riskReward: "2.0:1",
    explanation: "Gold is showing constructive compression with stable historical follow-through."
  },
  {
    rank: 4,
    symbol: "XBI",
    category: "Biotech",
    currentPrice: "160.46",
    priceChange: "+3.91",
    priceChangePercent: "+2.5%",
    priceTone: "mint",
    priceSource: "yfinance delayed fallback",
    priceAsOf: "2026-07-02 close",
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
    entry: "162.20",
    stop: "153.40",
    target: "178.50",
    riskReward: "1.9:1",
    explanation: "Biotech is improving, though confirmation is still less decisive than the top-ranked opportunities."
  },
  {
    rank: 5,
    symbol: "IBIT",
    category: "Crypto Bitcoin",
    currentPrice: "34.87",
    priceChange: "+0.87",
    priceChangePercent: "+2.6%",
    priceTone: "mint",
    priceSource: "yfinance delayed fallback",
    priceAsOf: "2026-07-02 close",
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
    entry: "35.40",
    stop: "32.80",
    target: "40.60",
    riskReward: "2.0:1",
    explanation: "Bitcoin exposure is compressing near resistance with improving volume confirmation."
  },
  {
    rank: 6,
    symbol: "ETHA",
    category: "Crypto Ethereum",
    currentPrice: "12.86",
    priceChange: "+0.67",
    priceChangePercent: "+5.5%",
    priceTone: "mint",
    priceSource: "yfinance delayed fallback",
    priceAsOf: "2026-07-02 close",
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
    entry: "13.10",
    stop: "11.90",
    target: "15.30",
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
    name: "Historical Bearish Analog",
    quality: 64,
    historicalAccuracy: 58,
    predictionScore: 58,
    breakoutProbability: 34,
    breakdownProbability: 58,
    keyLevel: "59.90",
    currentPrice: "61.96",
    predictedMove: "Sell trigger forming",
    confidence: "Medium",
    direction: "Bearish",
    evidence: ["split-adjusted delayed price 61.96", "historical analogs lean bearish", "live API confirmation required"],
    summary: "Historical Bearish Analog has a 58/100 AI chart score with support near 59.90."
  },
  {
    symbol: "SOXL",
    name: "Gap Breakout",
    quality: 84,
    historicalAccuracy: 62,
    predictionScore: 78,
    breakoutProbability: 78,
    breakdownProbability: 14,
    keyLevel: "184.00",
    currentPrice: "181.47",
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
    keyLevel: "35.40",
    currentPrice: "34.87",
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
