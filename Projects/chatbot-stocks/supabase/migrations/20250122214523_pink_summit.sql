/*
  # Add stock symbols table

  1. New Tables
    - `stock_symbols`
      - `id` (uuid, primary key)
      - `symbol` (text, unique)
      - `company_name` (text)
      - `type` (text)
      - `exchange` (text)
      - `currency` (text)
      - `sector` (text, nullable)
      - `industry` (text, nullable)
      - `last_updated` (timestamptz)
      - `created_at` (timestamptz)

  2. Security
    - Enable RLS on `stock_symbols` table
    - Add policy for public read access
    - Add policy for authenticated users to update
*/

CREATE TABLE IF NOT EXISTS stock_symbols (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  symbol text UNIQUE NOT NULL,
  company_name text NOT NULL,
  type text NOT NULL,
  exchange text NOT NULL,
  currency text NOT NULL,
  sector text,
  industry text,
  last_updated timestamptz NOT NULL DEFAULT now(),
  created_at timestamptz NOT NULL DEFAULT now()
);

-- Enable RLS
ALTER TABLE stock_symbols ENABLE ROW LEVEL SECURITY;

-- Allow public read access
CREATE POLICY "Allow public read access to stock symbols"
  ON stock_symbols
  FOR SELECT
  TO public
  USING (true);

-- Allow authenticated users to update
CREATE POLICY "Allow authenticated users to update stock symbols"
  ON stock_symbols
  FOR UPDATE
  TO authenticated
  USING (true)
  WITH CHECK (true);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_stock_symbols_symbol ON stock_symbols(symbol);
CREATE INDEX IF NOT EXISTS idx_stock_symbols_company_name ON stock_symbols(company_name);
CREATE INDEX IF NOT EXISTS idx_stock_symbols_exchange ON stock_symbols(exchange);