import React, { useState, useRef, useEffect } from 'react';
import { Search, TrendingUp, MessageSquare, ArrowUp, ArrowDown, Info } from 'lucide-react';
import { format } from 'date-fns';
import type { ChatMessage, StockQuote } from './types';
import { FinnhubService, STOCK_ALIASES } from './services/finnhub';
import { OpenAIService } from './services/openai';

const finnhubService = FinnhubService.getInstance();
const openaiService = OpenAIService.getInstance();

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [marketOverview, setMarketOverview] = useState<StockQuote[]>([]);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const chatContainerRef = useRef<HTMLDivElement>(null);

  const loadMarketOverview = async () => {
    try {
      setError(null);
      const symbols = finnhubService.getDefaultStocks();
      const quotes = await Promise.all(
        symbols.map(async (symbol) => {
          const quote = await finnhubService.getQuote(symbol);
          return quote;
        })
      );
      
      if (quotes.some(quote => quote.c > 0)) {
        setMarketOverview(quotes);
      } else {
        setError('Unable to fetch market data. Please try again later.');
      }

      const interval = setInterval(async () => {
        try {
          const updatedQuotes = await Promise.all(
            symbols.map(async (symbol) => {
              const quote = await finnhubService.getQuote(symbol);
              return quote;
            })
          );
          if (updatedQuotes.some(quote => quote.c > 0)) {
            setMarketOverview(updatedQuotes);
            setError(null);
          }
        } catch (err) {
          console.error('Error updating market data:', err);
          setError('Unable to update market data. Will retry in 5 minutes.');
        }
      }, 300000);

      return () => clearInterval(interval);
    } catch (err) {
      console.error('Error loading market overview:', err);
      setError('Unable to load market data. Please try again later.');
    }
  };

  useEffect(() => {
    loadMarketOverview();
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim()) return;
    
    setLoading(true);
    try {
      const userMessage: ChatMessage = {
        id: crypto.randomUUID(),
        content: message,
        role: 'user',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, userMessage]);

      // Check if the message contains a stock symbol
      let symbol = finnhubService.getSymbolFromText(message);
      let stockData = null;
      if (symbol) {
        stockData = await finnhubService.getQuote(symbol);
      }

      // Get market trends
      const trends = await finnhubService.getMarketTrends();

      // Generate response using OpenAI
      const response = await openaiService.generateResponse(
        message,
        trends,
        stockData ? { symbol, quote: stockData } : undefined
      );

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        content: response,
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, assistantMessage]);

      setMessage('');
    } catch (error) {
      console.error('Error processing message:', error);
      const errorMessage: ChatMessage = {
        id: crypto.randomUUID(),
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        role: 'assistant',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const renderMarketOverview = () => {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Market Overview</h2>
          <div className="flex items-center space-x-2 text-sm text-gray-500">
            <Info className="h-4 w-4" />
            <span>Auto-updates every 5 minutes</span>
          </div>
        </div>

        <div className="space-y-4">
          {marketOverview.map((quote) => (
            <div key={quote.symbol} 
              className="bg-white rounded-lg p-4 shadow-sm hover:shadow-md transition-shadow duration-200">
              <div className="flex justify-between items-center">
                <div>
                  <span className="font-medium text-lg">{quote.symbol}</span>
                  <p className="text-sm text-gray-500">
                    {Object.entries(STOCK_ALIASES).find(([symbol]) => symbol === quote.symbol)?.[1][0]}
                  </p>
                </div>
                <div className="text-right">
                  <div className="font-semibold text-lg">${quote.c.toFixed(2)}</div>
                  <div className={`flex items-center space-x-1 ${
                    quote.dp > 0 ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {quote.dp > 0 ? (
                      <ArrowUp className="h-4 w-4" />
                    ) : (
                      <ArrowDown className="h-4 w-4" />
                    )}
                    <span className="font-medium">
                      {quote.d > 0 ? '+' : ''}{quote.d.toFixed(2)} ({quote.dp.toFixed(2)}%)
                    </span>
                  </div>
                </div>
              </div>
              <div className="mt-2 text-sm text-gray-500">
                <div className="flex justify-between">
                  <span>Open</span>
                  <span>${quote.o.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>High</span>
                  <span>${quote.h.toFixed(2)}</span>
                </div>
                <div className="flex justify-between">
                  <span>Low</span>
                  <span>${quote.l.toFixed(2)}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-6 w-6 text-indigo-600" />
              <h1 className="text-xl font-bold text-gray-900">StockChat AI</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow-sm">
              <div className="h-[600px] flex flex-col">
                <div 
                  ref={chatContainerRef}
                  className="flex-1 p-4 overflow-y-auto"
                >
                  {messages.length === 0 ? (
                    <div className="flex items-center justify-center h-full text-gray-500">
                      <div className="text-center">
                        <MessageSquare className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                        <p>Start a conversation about stocks!</p>
                        <p className="text-sm">Try asking about specific stocks or market trends</p>
                      </div>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {messages.map((msg) => (
                        <div
                          key={msg.id}
                          className={`flex ${
                            msg.role === 'user' ? 'justify-end' : 'justify-start'
                          }`}
                        >
                          <div
                            className={`rounded-lg px-4 py-2 max-w-[80%] ${
                              msg.role === 'user'
                                ? 'bg-indigo-600 text-white'
                                : 'bg-gray-100 text-gray-900'
                            }`}
                          >
                            <p className="whitespace-pre-line">{msg.content}</p>
                            <p
                              className={`text-xs mt-1 ${
                                msg.role === 'user'
                                  ? 'text-indigo-200'
                                  : 'text-gray-500'
                              }`}
                            >
                              {format(msg.timestamp, 'HH:mm')}
                            </p>
                          </div>
                        </div>
                      ))}
                      <div ref={messagesEndRef} />
                    </div>
                  )}
                </div>

                <form onSubmit={handleSubmit} className="border-t p-4">
                  <div className="flex space-x-4">
                    <input
                      type="text"
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      placeholder="Ask about any stock..."
                      className="flex-1 rounded-lg border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      disabled={loading}
                    />
                    <button
                      type="submit"
                      disabled={loading}
                      className="bg-indigo-600 text-white px-6 py-2 rounded-lg hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50"
                    >
                      Send
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-sm p-6">
            {error ? (
              <div className="text-center py-8">
                <TrendingUp className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <p className="text-gray-500 mb-4">{error}</p>
                <button
                  onClick={() => {
                    setError(null);
                    loadMarketOverview();
                  }}
                  className="text-indigo-600 hover:text-indigo-700 font-medium"
                >
                  Try Again
                </button>
              </div>
            ) : marketOverview.length > 0 ? (
              renderMarketOverview()
            ) : (
              <div className="animate-pulse">
                <div className="h-4 bg-gray-200 rounded w-3/4"></div>
                <div className="space-y-3 mt-4">
                  <div className="h-4 bg-gray-200 rounded"></div>
                  <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;