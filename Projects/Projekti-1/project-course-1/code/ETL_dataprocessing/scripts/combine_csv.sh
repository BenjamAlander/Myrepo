# Vaihtoehtoinen tapa luoda yksi filu kaikista csv tiedostoista. Poistaa otsikot joka csv:stä. Muokkaa vikan rivin kommenttia sen mukaan haluatko että alkuperäinen data poistetaan.

#!/bin/bash

# Get all CSV files in the current directory
csv_files=$(ls *.csv 2>/dev/null)

# If there are no CSV files, print an error message and exit
if [ -z "$csv_files" ]; then
  echo "No CSV files found in the current directory."
  exit 1
fi

# Combine all CSV files into a single file
cat $csv_files > combined_data.csv

# Delete the original CSV files
rm $csv_files
