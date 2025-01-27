/*
  # Add Historical Stock Data Tables

  1. New Tables
    - `stock_historical_data`
      - `id` (uuid, primary key)
      - `symbol` (text)
      - `date` (timestamptz)
      - `open` (numeric)
      - `high` (numeric)
      - `low` (numeric)
      - `close` (numeric)
      - `volume` (numeric)
      - `created_at` (timestamptz)

    - `stock_analysis`
      - `id` (uuid, primary key)
      - `symbol` (text)
      - `date` (timestamptz)
      - `ma_50` (numeric)
      - `ma_200` (numeric)
      - `rsi` (numeric)
      - `volatility` (numeric)
      - `trend` (text)
      - `recommendation` (text)
      - `created_at` (timestamptz)

  2. Security
    - Enable RLS on both tables
    - Add policies for read access
*/

CREATE TABLE IF NOT EXISTS stock_historical_data (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  symbol text NOT NULL,
  date timestamptz NOT NULL,
  open numeric NOT NULL,
  high numeric NOT NULL,
  low numeric NOT NULL,
  close numeric NOT NULL,
  volume numeric NOT NULL,
  created_at timestamptz DEFAULT now(),
  UNIQUE(symbol, date)
);

CREATE TABLE IF NOT EXISTS stock_analysis (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  symbol text NOT NULL,
  date timestamptz NOT NULL,
  ma_50 numeric,
  ma_200 numeric,
  rsi numeric,
  volatility numeric,
  trend text,
  recommendation text,
  support_level numeric,
  resistance_level numeric,
  volume_trend text,
  created_at timestamptz DEFAULT now(),
  UNIQUE(symbol, date)
);

ALTER TABLE stock_historical_data ENABLE ROW LEVEL SECURITY;
ALTER TABLE stock_analysis ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access to historical data"
  ON stock_historical_data
  FOR SELECT
  TO public
  USING (true);

CREATE POLICY "Allow public read access to stock analysis"
  ON stock_analysis
  FOR SELECT
  TO public
  USING (true);

CREATE INDEX idx_historical_data_symbol_date ON stock_historical_data(symbol, date);
CREATE INDEX idx_stock_analysis_symbol_date ON stock_analysis(symbol, date);