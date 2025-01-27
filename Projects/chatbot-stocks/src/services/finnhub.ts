import axios, { AxiosError } from 'axios';
import type { StockQuote, CompanyProfile, FinancialMetrics, MarketTrends } from '../types';
import { supabase } from './supabase';

const FINNHUB_API_KEY = 'cu8hkqpr01qt63vh18u0cu8hkqpr01qt63vh18ug';
const BASE_URL = 'https://finnhub.io/api/v1';
const MAX_RETRIES = 3;
const RETRY_DELAY = 1000;

// Stock symbol aliases for better display
export const STOCK_ALIASES: Record<string, string[]> = {
  'AAPL': ['Apple Inc.', 'Apple'],
  'MSFT': ['Microsoft Corporation', 'Microsoft'],
  'GOOGL': ['Alphabet Inc.', 'Google'],
  'AMZN': ['Amazon.com Inc.', 'Amazon'],
  'META': ['Meta Platforms Inc.', 'Facebook'],
  'TSLA': ['Tesla Inc.', 'Tesla'],
  'NVDA': ['NVIDIA Corporation', 'NVIDIA'],
  'JPM': ['JPMorgan Chase & Co.', 'JPMorgan'],
  'V': ['Visa Inc.', 'Visa'],
  'JNJ': ['Johnson & Johnson', 'J&J']
};

export class FinnhubService {
  private static instance: FinnhubService;
  private rateLimitQueue: Promise<void>;
  private cachedQuotes: Map<string, { quote: StockQuote; timestamp: number }>;
  private cachedSymbols: Map<string, string[]>;
  private readonly CACHE_DURATION = 60000; // 1 minute cache
  private readonly SYMBOLS_CACHE_DURATION = 3600000; // 1 hour cache

  private constructor() {
    this.rateLimitQueue = Promise.resolve();
    this.cachedQuotes = new Map();
    this.cachedSymbols = new Map();
    this.initializeSymbolCache();
  }

  static getInstance(): FinnhubService {
    if (!FinnhubService.instance) {
      FinnhubService.instance = new FinnhubService();
    }
    return FinnhubService.instance;
  }

  private async initializeSymbolCache(): Promise<void> {
    try {
      const { data: symbols, error } = await supabase
        .from('stock_symbols')
        .select('symbol, sector')
        .order('symbol');

      if (error) throw error;

      symbols.forEach(({ symbol, sector }) => {
        const sectorKey = sector?.toLowerCase() || 'unknown';
        if (!this.cachedSymbols.has(sectorKey)) {
          this.cachedSymbols.set(sectorKey, []);
        }
        this.cachedSymbols.get(sectorKey)?.push(symbol);
      });
    } catch (error) {
      console.error('Error initializing symbol cache:', error);
    }
  }

  private async delay(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  private async executeWithRetry<T>(operation: () => Promise<T>, retries = MAX_RETRIES): Promise<T> {
    try {
      return await new Promise((resolve, reject) => {
        this.rateLimitQueue = this.rateLimitQueue
          .then(async () => {
            try {
              const result = await operation();
              resolve(result);
            } catch (error) {
              reject(error);
            }
            await this.delay(100);
          });
      });
    } catch (error) {
      if (retries > 0 && error instanceof Error) {
        const isRateLimit = error instanceof AxiosError && 
          (error.response?.status === 429 || error.response?.status === 403);
        const delayTime = isRateLimit ? RETRY_DELAY * 2 : RETRY_DELAY;
        await this.delay(delayTime);
        return this.executeWithRetry(operation, retries - 1);
      }
      throw error;
    }
  }

  getDefaultStocks(): string[] {
    return Object.keys(STOCK_ALIASES);
  }

  async getAllSymbols(): Promise<string[]> {
    const allSymbols: string[] = [];
    this.cachedSymbols.forEach(symbols => {
      allSymbols.push(...symbols);
    });
    return allSymbols;
  }

  async getSymbolsBySector(sector: string): Promise<string[]> {
    return this.cachedSymbols.get(sector.toLowerCase()) || [];
  }

  async getSectors(): Promise<string[]> {
    return Array.from(this.cachedSymbols.keys());
  }

  async getQuote(symbol: string): Promise<StockQuote> {
    try {
      const cached = this.cachedQuotes.get(symbol);
      if (cached && Date.now() - cached.timestamp < this.CACHE_DURATION) {
        return cached.quote;
      }

      const response = await this.executeWithRetry(() =>
        axios.get(`${BASE_URL}/quote`, {
          params: {
            symbol,
            token: FINNHUB_API_KEY
          }
        })
      );

      const quote: StockQuote = {
        symbol,
        c: response.data.c || 0,
        d: response.data.d || 0,
        dp: response.data.dp || 0,
        h: response.data.h || 0,
        l: response.data.l || 0,
        o: response.data.o || 0,
        pc: response.data.pc || 0,
        t: response.data.t || Date.now()
      };

      this.cachedQuotes.set(symbol, {
        quote,
        timestamp: Date.now()
      });

      return quote;
    } catch (error) {
      console.error('Error fetching quote:', error);
      throw error;
    }
  }

  async getCompanyProfile(symbol: string): Promise<CompanyProfile | null> {
    try {
      const response = await this.executeWithRetry(() =>
        axios.get(`${BASE_URL}/stock/profile2`, {
          params: {
            symbol,
            token: FINNHUB_API_KEY
          }
        })
      );

      return response.data;
    } catch (error) {
      console.error('Error fetching company profile:', error);
      return null;
    }
  }

  async getFinancialMetrics(symbol: string): Promise<FinancialMetrics | null> {
    try {
      const response = await this.executeWithRetry(() =>
        axios.get(`${BASE_URL}/stock/metric`, {
          params: {
            symbol,
            metric: 'all',
            token: FINNHUB_API_KEY
          }
        })
      );

      return response.data;
    } catch (error) {
      console.error('Error fetching financial metrics:', error);
      return null;
    }
  }

  async getMarketTrends(): Promise<MarketTrends> {
    try {
      const defaultStocks = this.getDefaultStocks();
      const quotes = await Promise.all(
        defaultStocks.map(symbol => this.getQuote(symbol))
      );

      const gainers = quotes.filter(q => q.dp > 0).sort((a, b) => b.dp - a.dp);
      const losers = quotes.filter(q => q.dp < 0).sort((a, b) => a.dp - b.dp);
      const averageChange = quotes.reduce((acc, q) => acc + q.dp, 0) / quotes.length;

      const sectors = {
        'Technology': {
          performance: 0,
          trend: 'neutral' as const
        },
        'Finance': {
          performance: 0,
          trend: 'neutral' as const
        },
        'Healthcare': {
          performance: 0,
          trend: 'neutral' as const
        }
      };

      return {
        sectors,
        topGainers: gainers.slice(0, 5),
        topLosers: losers.slice(0, 5),
        mostActive: quotes.sort((a, b) => Math.abs(b.dp) - Math.abs(a.dp)).slice(0, 5),
        overallMarket: {
          trend: averageChange > 0.5 ? 'bullish' : averageChange < -0.5 ? 'bearish' : 'neutral',
          averageChange,
          gainers: gainers.length,
          losers: losers.length
        }
      };
    } catch (error) {
      console.error('Error fetching market trends:', error);
      throw error;
    }
  }

  getSymbolFromText(text: string): string | null {
    const words = text.toUpperCase().split(/\s+/);
    for (const word of words) {
      if (STOCK_ALIASES[word]) {
        return word;
      }
    }
    return null;
  }
}