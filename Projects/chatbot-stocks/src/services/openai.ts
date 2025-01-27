import OpenAI from 'openai';
import type { StockQuote, MarketTrends } from '../types';
import { supabase } from './supabase';

const BASE_SYSTEM_INSTRUCTIONS = `You are StockChat AI, a professional financial assistant specializing in stock market analysis and insights. You have access to real-time market data and can provide information about stocks, market trends, and company performance.

Guidelines:
- Maintain a professional, formal tone
- Keep responses concise and informative
- Use bullet points for structured information
- Focus on actionable insights and data-driven analysis
- Acknowledge when specific data is not available
- Stay within your knowledge domain of finance and markets

When analyzing stocks:
1. Consider both technical and fundamental factors
2. Provide context for market conditions
3. Compare against sector peers when relevant
4. Discuss potential risks and opportunities
5. Reference relevant market trends

Available Real-Time Data:
- Live stock quotes
- Daily price changes
- Market trends
- Sector performance
- Top gainers and losers`;

export class OpenAIService {
  private static instance: OpenAIService;
  private openai: OpenAI;
  private conversationHistory: { role: 'system' | 'user' | 'assistant'; content: string }[];
  private stockSymbols: Map<string, string[]> = new Map();
  private lastSymbolUpdate: number = 0;
  private readonly SYMBOL_UPDATE_INTERVAL = 24 * 60 * 60 * 1000; // 24 hours

  private constructor() {
    this.openai = new OpenAI({
      apiKey: import.meta.env.VITE_OPENAI_API_KEY,
      dangerouslyAllowBrowser: true
    });
    this.conversationHistory = [
      { role: 'system', content: BASE_SYSTEM_INSTRUCTIONS }
    ];
  }

  static getInstance(): OpenAIService {
    if (!OpenAIService.instance) {
      OpenAIService.instance = new OpenAIService();
    }
    return OpenAIService.instance;
  }

  private async updateStockSymbols(): Promise<void> {
    const now = Date.now();
    if (now - this.lastSymbolUpdate < this.SYMBOL_UPDATE_INTERVAL) {
      return;
    }

    try {
      const { data: symbols, error } = await supabase
        .from('stock_symbols')
        .select('*')
        .order('symbol');

      if (error) throw error;

      this.stockSymbols.clear();
      symbols?.forEach(symbol => {
        const sector = symbol.sector?.toLowerCase() || 'unknown';
        if (!this.stockSymbols.has(sector)) {
          this.stockSymbols.set(sector, []);
        }
        this.stockSymbols.get(sector)?.push(symbol.symbol);
      });

      this.lastSymbolUpdate = now;

      // Update system instructions with current stock coverage
      const sectorInstructions = Array.from(this.stockSymbols.entries())
        .map(([sector, symbols]) => `   - ${sector.charAt(0).toUpperCase() + sector.slice(1)}: ${symbols.join(', ')}`)
        .join('\n');

      const updatedInstructions = `${BASE_SYSTEM_INSTRUCTIONS}

Stock Market Coverage:
1. Major US Stock Exchanges:
   - NYSE
   - NASDAQ
   - AMEX

2. Sectors:
${sectorInstructions}`;

      // Update the first system message
      this.conversationHistory[0].content = updatedInstructions;
    } catch (error) {
      console.error('Error updating stock symbols:', error);
    }
  }

  private formatMarketData(marketData: MarketTrends): string {
    return `
Current Market Data:
- Overall Market Trend: ${marketData.overallMarket.trend}
- Average Market Change: ${marketData.overallMarket.averageChange.toFixed(2)}%
- Gainers vs Losers: ${marketData.overallMarket.gainers}/${marketData.overallMarket.losers}

Sector Performance:
${Object.entries(marketData.sectors)
  .map(([sector, data]) => `- ${sector}: ${data.performance.toFixed(2)}% (${data.trend})`)
  .join('\n')}

Top Gainers:
${marketData.topGainers
  .map(stock => `- ${stock.symbol}: +${stock.dp.toFixed(2)}%`)
  .join('\n')}

Top Losers:
${marketData.topLosers
  .map(stock => `- ${stock.symbol}: ${stock.dp.toFixed(2)}%`)
  .join('\n')}`;
  }

  private formatStockData(symbol: string, quote: StockQuote): string {
    return `
Stock Data for ${symbol}:
- Current Price: $${quote.c}
- Daily Change: ${quote.dp > 0 ? '+' : ''}${quote.dp.toFixed(2)}%
- Daily Range: $${quote.l} - $${quote.h}
- Previous Close: $${quote.pc}`;
  }

  async generateResponse(
    userMessage: string,
    marketData?: MarketTrends,
    stockData?: { symbol: string; quote: StockQuote }
  ): Promise<string> {
    try {
      // Update stock symbols if needed
      await this.updateStockSymbols();

      let contextMessage = 'Current Market Analysis:\n\n';
      
      if (marketData) {
        contextMessage += this.formatMarketData(marketData);
      }
      
      if (stockData) {
        contextMessage += '\n\n' + this.formatStockData(stockData.symbol, stockData.quote);
      }

      // Add user's message to history
      this.conversationHistory.push({ role: 'user', content: userMessage });
      
      // Add context as a system message
      if (marketData || stockData) {
        this.conversationHistory.push({ role: 'system', content: contextMessage });
      }

      // Keep only last 10 messages to prevent token limit issues
      if (this.conversationHistory.length > 10) {
        this.conversationHistory = [
          this.conversationHistory[0], // Keep system instructions
          ...this.conversationHistory.slice(-9) // Keep last 9 messages
        ];
      }

      const response = await this.openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: this.conversationHistory,
        temperature: 0.7,
        max_tokens: 500
      });

      const assistantMessage = response.choices[0].message.content || 
        "I apologize, but I'm having trouble generating a response at the moment.";

      // Add assistant's response to history
      this.conversationHistory.push({ role: 'assistant', content: assistantMessage });

      return assistantMessage;
    } catch (error) {
      console.error('Error generating response:', error);
      return "I apologize, but I'm having trouble processing your request at the moment.";
    }
  }
}