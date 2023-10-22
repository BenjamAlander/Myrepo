import csv

# define input and output filenames
input_filename = 'code\data\combined_data_cleaned4.csv'
output_filename = 'code\data\combined_data_cleaned5.csv'

# open input and output files
with open(input_filename, 'r') as input_file, open(output_filename, 'w', newline='') as output_file:
    # create csv reader and writer objects
    reader = csv.reader(input_file)
    writer = csv.writer(output_file)

    # write header row to output file
    header = next(reader)
    writer.writerow(header)

    # loop through each row in input file
    for row in reader:
        # check if row has enough columns
        if len(row) >= 4:
            try:
                # convert x and y values to integers
                x, y = int(row[2]), int(row[3])

                # apply filtering on x and y values
                if (0 < x < 10406 and 0 < y < 5220 and not (y > 3000 and x < 1540) and not (y < 522 and x > 8350) and not (x > 9900 and y > 4700)and not(x < 1500 and y > 3000 and y < 3500) and not(x < 600 and y > 2000 and y < 3000)):
                    # write row to output file if x and y values are within limits and do not meet exclusion criteria   MUOKKAA YLEMPÄÄ KOODIA        
                    writer.writerow(row)
            except ValueError:
                # ignore rows with invalid x or y values
                pass
    print("done")


