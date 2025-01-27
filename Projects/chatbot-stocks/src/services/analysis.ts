import { supabase } from './supabase';
import { FinnhubService } from './finnhub';
import type { StockAnalysis, HistoricalDataPoint } from '../types';

export class AnalysisService {
  private static instance: AnalysisService;
  private finnhubService: FinnhubService;

  private constructor() {
    this.finnhubService = FinnhubService.getInstance();
  }

  static getInstance(): AnalysisService {
    if (!AnalysisService.instance) {
      AnalysisService.instance = new AnalysisService();
    }
    return AnalysisService.instance;
  }

  async storeHistoricalData(symbol: string, data: HistoricalDataPoint[]): Promise<void> {
    const { error } = await supabase
      .from('stock_historical_data')
      .upsert(
        data.map(point => ({
          symbol,
          date: point.date,
          open: point.open,
          high: point.high,
          low: point.low,
          close: point.close,
          volume: point.volume
        }))
      );

    if (error) throw error;
  }

  async storeAnalysis(symbol: string, analysis: StockAnalysis): Promise<void> {
    const { error } = await supabase
      .from('stock_analysis')
      .upsert({
        symbol,
        date: new Date(),
        ma_50: analysis.technicals.ma50,
        ma_200: analysis.technicals.ma200,
        rsi: analysis.metrics.rsi,
        volatility: analysis.technicals.volatility,
        trend: JSON.stringify(analysis.technicals.trend),
        recommendation: analysis.recommendation,
        support_level: analysis.levels.support,
        resistance_level: analysis.levels.resistance,
        volume_trend: analysis.technicals.volumeTrend
      });

    if (error) throw error;
  }

  async getHistoricalData(symbol: string, days: number = 365): Promise<HistoricalDataPoint[]> {
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);

    const { data, error } = await supabase
      .from('stock_historical_data')
      .select('*')
      .eq('symbol', symbol)
      .gte('date', startDate.toISOString())
      .order('date', { ascending: true });

    if (error) throw error;
    return data as HistoricalDataPoint[];
  }

  async getLatestAnalysis(symbol: string): Promise<StockAnalysis | null> {
    const { data, error } = await supabase
      .from('stock_analysis')
      .select('*')
      .eq('symbol', symbol)
      .order('date', { ascending: false })
      .limit(1)
      .single();

    if (error) return null;
    if (!data) return null;

    return {
      symbol: data.symbol,
      currentPrice: 0, // Will be updated with current price
      metrics: {
        pe: 0, // Will be updated with current metrics
        pb: 0,
        beta: 0,
        rsi: data.rsi
      },
      technicals: {
        ma50: data.ma_50,
        ma200: data.ma_200,
        volatility: data.volatility,
        volumeTrend: data.volume_trend,
        trend: JSON.parse(data.trend)
      },
      levels: {
        support: data.support_level,
        resistance: data.resistance_level
      },
      recommendation: data.recommendation
    };
  }

  async updateHistoricalData(symbol: string): Promise<void> {
    const history = await this.finnhubService.getHistoricalData(
      symbol,
      new Date(Date.now() - 365 * 24 * 60 * 60 * 1000)
    );

    if (!history) return;

    const dataPoints: HistoricalDataPoint[] = history.t.map((timestamp, index) => ({
      date: new Date(timestamp * 1000),
      open: history.o[index],
      high: history.h[index],
      low: history.l[index],
      close: history.c[index],
      volume: history.v[index]
    }));

    await this.storeHistoricalData(symbol, dataPoints);
  }

  async updateAnalysis(symbol: string): Promise<void> {
    const analysis = await this.finnhubService.getStockAnalysis(symbol);
    if (analysis) {
      await this.storeAnalysis(symbol, analysis);
    }
  }

  async getFullAnalysis(symbol: string): Promise<StockAnalysis | null> {
    try {
      // Update historical data and analysis
      await Promise.all([
        this.updateHistoricalData(symbol),
        this.updateAnalysis(symbol)
      ]);

      // Get the latest analysis
      return await this.getLatestAnalysis(symbol);
    } catch (error) {
      console.error('Error getting full analysis:', error);
      return null;
    }
  }
}