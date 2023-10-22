import csv

# Open CSV file for reading and writing
with open('code/data/combined_data_cleaned4.csv', 'r+', newline='') as infile:

    # Create CSV reader and writer objects
    reader = csv.reader(infile, delimiter=',')
    writer = csv.writer(infile, delimiter=',')

    # Write header row to output file
    header = next(reader)
    writer.writerow(header)

    # Write data rows to output file, skipping extra header rows
    for row in reader:
        if row != header:
            writer.writerow(row)
