import pandas as pd

# Define the chunk size
chunk_size = 100000

# Define the csv2pandas class
class csv2pandas:
    def __init__(self, csv_file="combined_data.csv"):
        self.csv_file = csv_file

    def read_csv(self):
        # Create an empty list to hold the chunks
        chunks = []

        # Loop through the file in chunks and append to the list
        for chunk in pd.read_csv(self.csv_file, low_memory=False, chunksize=chunk_size):

            # Convert the 'timestamp' column to string and extract the first 16 characters
            chunk['timestamp'] = chunk['timestamp'].astype(str).str[:16]

            # Append the modified chunk to the list
            chunks.append(chunk)

        # Concatenate the chunks into a single dataframe
        df = pd.concat(chunks, ignore_index=True)

        return df

# Create an instance of the csv2pandas class
reader = csv2pandas()

# Call the read_csv method to read the CSV file into a pandas dataframe
dataframe = reader.read_csv()

# Write the cleaned data to a new CSV file
dataframe.to_csv('combined_data_cleaned2.csv', index=False)
