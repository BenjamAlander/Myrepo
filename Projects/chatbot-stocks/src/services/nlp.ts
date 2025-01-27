import nlp from 'compromise';
import { supabase } from './supabase';
import type { NLPAnalysis, StockQuote, FinancialMetrics } from '../types';
import { FinnhubService } from './finnhub';
import { OpenAIService } from './openai';

const finnhubService = FinnhubService.getInstance();
const openaiService = OpenAIService.getInstance();

export class NLPService {
  private static instance: NLPService;
  private intentPatterns: Map<string, RegExp[]>;

  private constructor() {
    this.intentPatterns = new Map([
      ['price_query', [
        /(?:what(?:'s| is) (?:the )?(?:price|value|stock price) (?:of|for) .+)/i,
        /how (?:is|'s) .+ (?:doing|performing|trading)/i,
        /show me .+ stock/i,
        /tell me (?:about|more about) .+/i
      ]],
      ['market_overview', [
        /(?:how|what)(?:'s| is) (?:the )?market (?:doing|looking|today)/i,
        /market (?:overview|status|update|summary)/i,
        /(?:general|market) trends?/i
      ]],
      ['company_info', [
        /tell me (?:more )?about .+/i,
        /what (?:do you know|can you tell me) about .+/i,
        /(?:more )?information (?:about|on|for) .+/i
      ]],
      ['financial_metrics', [
        /(?:what are|show|tell me|get) (?:the )?(?:financial|key) (?:metrics|ratios|numbers|stats|statistics) (?:for|of) .+/i,
        /(?:p\/e|price to earnings|valuation|fundamentals|ratios) (?:of|for) .+/i
      ]],
      ['price_history', [
        /(?:show|display|get) (?:the )?(?:price|stock) (?:history|chart|trend|performance) (?:for|of) .+/i,
        /how has .+ (?:performed|done|been doing) (?:recently|lately|in the past|over time)/i
      ]]
    ]);
  }

  static getInstance(): NLPService {
    if (!NLPService.instance) {
      NLPService.instance = new NLPService();
    }
    return NLPService.instance;
  }

  private detectIntent(text: string): string {
    const normalizedText = text.toLowerCase();
    
    if (/^(?:hi|hello|hey|greetings)(?:\s|$)/i.test(normalizedText)) {
      return 'greeting';
    }

    if (/(?:help|guide|what can you do|how do you work)/i.test(normalizedText)) {
      return 'help';
    }

    for (const [intent, patterns] of this.intentPatterns.entries()) {
      if (patterns.some(pattern => pattern.test(text))) {
        return intent;
      }
    }

    return 'unknown';
  }

  private analyzeSentiment(text: string): string {
    const doc = nlp(text);
    const words = text.toLowerCase().split(/\s+/);
    
    const positiveWords = ['up', 'gain', 'gains', 'increase', 'higher', 'rising', 'rose', 'good', 'great', 'excellent', 'positive', 'bullish'];
    const negativeWords = ['down', 'loss', 'losses', 'decrease', 'lower', 'falling', 'fell', 'bad', 'poor', 'negative', 'bearish'];
    
    let score = 0;
    words.forEach(word => {
      if (positiveWords.includes(word)) score++;
      if (negativeWords.includes(word)) score--;
    });

    return score > 0 ? 'positive' : score < 0 ? 'negative' : 'neutral';
  }

  public async analyzeText(text: string): Promise<NLPAnalysis> {
    const doc = nlp(text);
    const intent = this.detectIntent(text);
    
    const organizations = doc.organizations().out('array');
    const values = doc.values().out('array');
    const money = doc.money().out('array');

    return {
      intent,
      entities: {
        organizations,
        values,
        money
      },
      sentiment: this.analyzeSentiment(text)
    };
  }

  public async generateResponse(analysis: NLPAnalysis, stockData: StockQuote | null = null): Promise<string> {
    try {
      // Handle market overview intent
      if (analysis.intent === 'market_overview' || /trend|general/i.test(analysis.entities.organizations.join(' '))) {
        const trends = await finnhubService.getMarketTrends();
        const response = await openaiService.generateMarketAnalysis(trends);
        
        // Format the response with proper markdown
        return response.split('\n').map(line => {
          if (line.startsWith('•')) {
            return line; // Keep bullet points as is
          }
          if (line.trim().endsWith(':')) {
            return `**${line.trim()}**`; // Bold headers
          }
          if (line.includes(':')) {
            const [key, value] = line.split(':');
            return `**${key.trim()}:** ${value.trim()}`; // Bold keys
          }
          return line;
        }).join('\n');
      }

      // Handle stock-specific queries
      let symbol = stockData?.symbol;
      if (!symbol && analysis.entities.organizations.length > 0) {
        const companyMatch = await openaiService.findCompanyMatch(analysis.entities.organizations.join(' '));
        if (companyMatch) {
          stockData = await finnhubService.getQuote(companyMatch);
          symbol = companyMatch;
        }
      }

      if (symbol && stockData) {
        const metrics = await finnhubService.getFinancialMetrics(symbol);
        const profile = await finnhubService.getCompanyProfile(symbol);
        return openaiService.generateStockAnalysis(symbol, stockData, metrics, profile);
      }

      // Handle general queries and unknown intents
      const context = {
        intent: analysis.intent,
        sentiment: analysis.sentiment,
        entities: analysis.entities
      };

      return openaiService.generateResponse(analysis.intent, context);
    } catch (error) {
      console.error('Error generating response:', error);
      return "I apologize, but I'm having trouble processing your request at the moment. Please try again.";
    }
  }
}