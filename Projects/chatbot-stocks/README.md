# StockChat AI 📈

An intelligent stock market chat assistant powered by AI, providing real-time market insights, stock analysis, and trading information through natural language conversations.

## Features

### Real-time Market Data 📊
- Live stock quotes and price updates
- Market trends and sector performance
- Top gainers and losers tracking
- Real-time market sentiment analysis

### Intelligent Chat Interface 🤖
- Natural language processing for stock queries
- Company information and financial metrics
- Technical analysis and price predictions
- Market sentiment and trend analysis

### Advanced Analytics 📉
- Historical price data analysis
- Technical indicators (RSI, Moving Averages)
- Support and resistance levels
- Volume analysis and trends

### Smart Features 🎯
- Company recognition from natural language
- Automatic stock symbol detection
- Multi-sector market analysis
- Customizable stock watchlists

## Prerequisites

Before running the project, you'll need:

1. Node.js 18+ installed
2. A Supabase account for the database
3. An OpenAI API key for AI features
4. A Finnhub API key for market data

## API Keys Setup

### 1. Finnhub API Key
1. Visit [Finnhub.io](https://finnhub.io)
2. Create a free account
3. Get your API key from the dashboard
4. Current key in the project: `cu8hkqpr01qt63vh18u0cu8hkqpr01qt63vh18ug`
   - Replace with your own key in `src/services/finnhub.ts`

### 2. OpenAI API Key
1. Visit [OpenAI Platform](https://platform.openai.com)
2. Create an account
3. Generate an API key
4. Add to your environment variables

### 3. Supabase Setup
1. Create a project at [Supabase](https://supabase.com)
2. Get your project URL and anon key
3. Add to your environment variables

## Environment Variables

Create a \`.env\` file in the root directory:

\`\`\`env
VITE_SUPABASE_ANON_KEY=your_supabase_anon_key
VITE_SUPABASE_URL=your_supabase_url
VITE_OPENAI_API_KEY=your_openai_api_key
\`\`\`

## Installation

1. Clone the repository:
\`\`\`bash
git clone https://github.com/yourusername/stockchat-ai.git
cd stockchat-ai
\`\`\`

2. Install dependencies:
\`\`\`bash
npm install
\`\`\`

3. Start the development server:
\`\`\`bash
npm run dev
\`\`\`

## Customization

### Modifying Tracked Stocks

Edit the \`STOCK_ALIASES\` in \`src/services/finnhub.ts\`:

\`\`\`typescript
export const STOCK_ALIASES: Record<string, string[]> = {
  'AAPL': ['Apple Inc.', 'Apple'],
  'MSFT': ['Microsoft Corporation', 'Microsoft'],
  // Add more stocks here
};
\`\`\`

### Adjusting Market Analysis Parameters

Modify market trend thresholds in \`src/services/finnhub.ts\`:

\`\`\`typescript
const averageChange = quotes.reduce((acc, q) => acc + q.dp, 0) / quotes.length;
return {
  trend: averageChange > 0.5 ? 'bullish' : averageChange < -0.5 ? 'bearish' : 'neutral',
  // Adjust thresholds as needed
};
\`\`\`

## Chat Commands

The chatbot understands various types of queries:

### Market Overview
- "How is the market today?"
- "Show me the market trends"
- "What's the general market sentiment?"

### Stock Queries
- "What's the price of AAPL?"
- "Tell me about Tesla stock"
- "How is Microsoft performing?"

### Analysis Requests
- "Show me the technical analysis for GOOGL"
- "What are the key metrics for Amazon?"
- "Give me a prediction for META"

### Sector Analysis
- "How is the tech sector doing?"
- "Show me top performing sectors"
- "Compare tech and finance sectors"

## Project Structure

\`\`\`
stockchat-ai/
├── src/
│   ├── services/
│   │   ├── finnhub.ts    # Market data service
│   │   ├── nlp.ts        # Natural language processing
│   │   ├── openai.ts     # AI integration
│   │   └── supabase.ts   # Database client
│   ├── types/
│   │   └── index.ts      # TypeScript definitions
│   └── App.tsx           # Main application
├── supabase/
│   └── migrations/       # Database schema
└── package.json
\`\`\`

## Contributing

1. Fork the repository
2. Create your feature branch: \`git checkout -b feature/amazing-feature\`
3. Commit your changes: \`git commit -m 'Add amazing feature'\`
4. Push to the branch: \`git push origin feature/amazing-feature\`
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.