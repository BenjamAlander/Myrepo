import csv
import time
start_time = time.time()
print("Program started")
num_rows = 0
with open('code\data\combined_data_cleaned5.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        num_rows += 1

print(num_rows)
print("----%s seconds ----" % (time.time()-start_time))



num_rows = 0
with open('code\data\combined_data_cleaned5.csv', 'r') as f:
    reader = csv.reader(f)
    for row in reader:
        print(row)
        num_rows += 1
        if num_rows == 20:
            break
