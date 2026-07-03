export type Opportunity = {
  rank: number;
  symbol: string;
  category: string;
  score: number;
  accuracy: number;
  confidence: "Very High" | "High" | "Medium" | "Low";
  matches: number;
  expectedReturn: string;
  window: string;
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

export const opportunities: Opportunity[] = [
  {
    rank: 1,
    symbol: "UVIX",
    category: "Volatility",
    score: 91,
    accuracy: 67,
    confidence: "Very High",
    matches: 84,
    expectedReturn: "+8.4%",
    window: "3-5 trading days",
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
  { name: "Volatility Expansion", quality: 91, accuracy: 67, confidence: "High", direction: "Bullish" },
  { name: "Gap Breakout", quality: 84, accuracy: 62, confidence: "Medium", direction: "Bullish" },
  { name: "Bull Flag", quality: 78, accuracy: 58, confidence: "Medium", direction: "Bullish" },
  { name: "Ascending Triangle", quality: 73, accuracy: 55, confidence: "Medium", direction: "Bullish" }
];

export const backtestRows = [
  { window: "3 days", trades: 84, winRate: "64%", avgReturn: "+4.1%", drawdown: "-2.2%", profitFactor: "1.54" },
  { window: "5 days", trades: 84, winRate: "67%", avgReturn: "+8.4%", drawdown: "-3.1%", profitFactor: "1.82" },
  { window: "8 days", trades: 79, winRate: "61%", avgReturn: "+7.2%", drawdown: "-4.6%", profitFactor: "1.39" }
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
