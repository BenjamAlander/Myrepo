/*
  # Fix Messages RLS Policies

  1. Changes
    - Add RLS policy to allow inserting messages for all users
    - Keep existing policy for reading messages

  2. Security
    - Enable RLS on messages table
    - Allow unrestricted inserts since this is a public chat
    - Maintain read access for authenticated users
*/

-- First ensure RLS is enabled
ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

-- Add policy to allow inserting messages
CREATE POLICY "Anyone can insert messages"
ON messages
FOR INSERT
TO public
WITH CHECK (true);

-- Keep existing read policy
CREATE POLICY "Authenticated users can read messages"
ON messages
FOR SELECT
TO authenticated
USING (true);