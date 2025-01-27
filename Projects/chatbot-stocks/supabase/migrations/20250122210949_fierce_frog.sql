/*
  # Add intent and sentiment columns to messages table

  1. Changes
    - Add `intent` column to store message intent (e.g., price_query, company_info)
    - Add `sentiment` column to store message sentiment (positive, negative, neutral)
    
  2. Security
    - Maintain existing RLS policies
*/

DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'messages' AND column_name = 'intent'
  ) THEN
    ALTER TABLE messages ADD COLUMN intent text;
  END IF;

  IF NOT EXISTS (
    SELECT 1 FROM information_schema.columns 
    WHERE table_name = 'messages' AND column_name = 'sentiment'
  ) THEN
    ALTER TABLE messages ADD COLUMN sentiment text;
  END IF;
END $$;