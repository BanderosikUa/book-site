import csv

file_path = '/home/banderosik/Downloads/main_dataset.csv'

with open(file_path) as csvfile:
    csvreader = csv.reader(csvfile)
    header = []
    header = next(csvreader)
    print(header)
    for row in csvreader:
        print(row)
