export interface StockQuote {
  symbol: string;
  c: number;    // Current price
  d: number;    // Change
  dp: number;   // Percent change
  h: number;    // High price of the day
  l: number;    // Low price of the day
  o: number;    // Open price of the day
  pc: number;   // Previous close price
  t: number;    // Timestamp
}

export interface ChatMessage {
  id: string;
  content: string;
  role: 'user' | 'assistant';
  timestamp: Date;
}

export interface CompanyProfile {
  country: string;
  currency: string;
  exchange: string;
  ipo: string;
  marketCapitalization: number;
  name: string;
  phone: string;
  shareOutstanding: number;
  ticker: string;
  weburl: string;
  logo: string;
  finnhubIndustry: string;
}

export interface FinancialMetrics {
  metric: {
    [key: string]: number | string | null;
  };
}

export interface MarketTrends {
  sectors: {
    [key: string]: {
      performance: number;
      trend: 'bullish' | 'bearish' | 'neutral';
    };
  };
  topGainers: StockQuote[];
  topLosers: StockQuote[];
  mostActive: StockQuote[];
  overallMarket: {
    trend: 'bullish' | 'bearish' | 'neutral';
    averageChange: number;
    gainers: number;
    losers: number;
  };
}

export interface NLPAnalysis {
  intent: string;
  entities: {
    organizations: string[];
    values: string[];
    money: string[];
  };
  sentiment: string;
}

export interface HistoricalDataPoint {
  date: Date;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

export interface StockAnalysis {
  symbol: string;
  currentPrice: number;
  metrics: {
    pe: number;
    pb: number;
    beta: number;
    rsi: number;
  };
  technicals: {
    ma50: number;
    ma200: number;
    volatility: number;
    volumeTrend: string;
    trend: {
      shortTerm: string;
      mediumTerm: string;
      longTerm: string;
    };
  };
  levels: {
    support: number;
    resistance: number;
  };
  recommendation: string;
}