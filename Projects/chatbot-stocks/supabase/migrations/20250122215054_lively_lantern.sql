/*
  # Update stock symbols table and policies

  1. Changes
    - Add IF NOT EXISTS checks for policies
    - Ensure policies are created only if they don't exist
*/

DO $$ 
BEGIN
  -- Create policies if they don't exist
  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE schemaname = 'public' 
    AND tablename = 'stock_symbols' 
    AND policyname = 'Allow public read access to stock symbols'
  ) THEN
    CREATE POLICY "Allow public read access to stock symbols"
      ON stock_symbols
      FOR SELECT
      TO public
      USING (true);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE schemaname = 'public' 
    AND tablename = 'stock_symbols' 
    AND policyname = 'Allow public to insert stock symbols'
  ) THEN
    CREATE POLICY "Allow public to insert stock symbols"
      ON stock_symbols
      FOR INSERT
      TO public
      WITH CHECK (true);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_policies 
    WHERE schemaname = 'public' 
    AND tablename = 'stock_symbols' 
    AND policyname = 'Allow authenticated users to update stock symbols'
  ) THEN
    CREATE POLICY "Allow authenticated users to update stock symbols"
      ON stock_symbols
      FOR UPDATE
      TO authenticated
      USING (true)
      WITH CHECK (true);
  END IF;

  -- Create indexes if they don't exist
  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes 
    WHERE schemaname = 'public' 
    AND tablename = 'stock_symbols' 
    AND indexname = 'idx_stock_symbols_symbol'
  ) THEN
    CREATE INDEX idx_stock_symbols_symbol ON stock_symbols(symbol);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes 
    WHERE schemaname = 'public' 
    AND tablename = 'stock_symbols' 
    AND indexname = 'idx_stock_symbols_company_name'
  ) THEN
    CREATE INDEX idx_stock_symbols_company_name ON stock_symbols(company_name);
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM pg_indexes 
    WHERE schemaname = 'public' 
    AND tablename = 'stock_symbols' 
    AND indexname = 'idx_stock_symbols_exchange'
  ) THEN
    CREATE INDEX idx_stock_symbols_exchange ON stock_symbols(exchange);
  END IF;
END $$;