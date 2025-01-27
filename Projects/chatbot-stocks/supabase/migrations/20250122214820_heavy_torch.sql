/*
  # Fix stock symbols RLS policies

  1. Changes
    - Add insert policy for stock symbols table to allow public inserts
    - Keep existing policies for read and update access

  2. Security
    - Maintains RLS
    - Allows public to insert new symbols
    - Maintains existing read/update policies
*/

-- Add policy to allow public to insert stock symbols
CREATE POLICY "Allow public to insert stock symbols"
  ON stock_symbols
  FOR INSERT
  TO public
  WITH CHECK (true);