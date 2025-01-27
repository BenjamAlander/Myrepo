/*
  # Expand stock market coverage

  1. New Data
    - Add more stocks to the stock_symbols table
    - Include stocks from various sectors and market caps
    - Add additional company metadata

  2. Changes
    - Insert comprehensive stock data
    - Add indexes for better query performance
*/

-- Insert more stock symbols with company data
INSERT INTO stock_symbols (symbol, company_name, type, exchange, currency, sector, industry)
VALUES
  -- Technology - Software
  ('ORCL', 'Oracle Corporation', 'stock', 'NYSE', 'USD', 'Technology', 'Software'),
  ('SAP', 'SAP SE', 'stock', 'NYSE', 'USD', 'Technology', 'Software'),
  ('NOW', 'ServiceNow Inc', 'stock', 'NYSE', 'USD', 'Technology', 'Software'),
  
  -- Technology - Semiconductors
  ('TSM', 'Taiwan Semiconductor Manufacturing', 'stock', 'NYSE', 'USD', 'Technology', 'Semiconductors'),
  ('QCOM', 'Qualcomm Inc', 'stock', 'NASDAQ', 'USD', 'Technology', 'Semiconductors'),
  ('TXN', 'Texas Instruments Inc', 'stock', 'NASDAQ', 'USD', 'Technology', 'Semiconductors'),
  
  -- Healthcare - Biotech
  ('AMGN', 'Amgen Inc', 'stock', 'NASDAQ', 'USD', 'Healthcare', 'Biotechnology'),
  ('GILD', 'Gilead Sciences Inc', 'stock', 'NASDAQ', 'USD', 'Healthcare', 'Biotechnology'),
  ('BIIB', 'Biogen Inc', 'stock', 'NASDAQ', 'USD', 'Healthcare', 'Biotechnology'),
  
  -- Finance - Insurance
  ('BRK.A', 'Berkshire Hathaway Inc', 'stock', 'NYSE', 'USD', 'Finance', 'Insurance'),
  ('AIG', 'American International Group', 'stock', 'NYSE', 'USD', 'Finance', 'Insurance'),
  ('MET', 'MetLife Inc', 'stock', 'NYSE', 'USD', 'Finance', 'Insurance'),
  
  -- Consumer Staples
  ('PG', 'Procter & Gamble Co', 'stock', 'NYSE', 'USD', 'Consumer Staples', 'Household Products'),
  ('KO', 'Coca-Cola Co', 'stock', 'NYSE', 'USD', 'Consumer Staples', 'Beverages'),
  ('PEP', 'PepsiCo Inc', 'stock', 'NASDAQ', 'USD', 'Consumer Staples', 'Beverages'),
  
  -- Energy - Clean Energy
  ('ENPH', 'Enphase Energy Inc', 'stock', 'NASDAQ', 'USD', 'Energy', 'Solar'),
  ('SEDG', 'SolarEdge Technologies', 'stock', 'NASDAQ', 'USD', 'Energy', 'Solar'),
  ('NEE', 'NextEra Energy Inc', 'stock', 'NYSE', 'USD', 'Energy', 'Utilities-Renewable'),
  
  -- Real Estate
  ('AMT', 'American Tower Corp', 'stock', 'NYSE', 'USD', 'Real Estate', 'REITs'),
  ('PLD', 'Prologis Inc', 'stock', 'NYSE', 'USD', 'Real Estate', 'REITs'),
  ('CCI', 'Crown Castle Inc', 'stock', 'NYSE', 'USD', 'Real Estate', 'REITs')
ON CONFLICT (symbol) DO UPDATE
SET 
  company_name = EXCLUDED.company_name,
  type = EXCLUDED.type,
  exchange = EXCLUDED.exchange,
  currency = EXCLUDED.currency,
  sector = EXCLUDED.sector,
  industry = EXCLUDED.industry,
  last_updated = now();