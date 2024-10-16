import csv

def printer(data, filename='output.csv'):
    # Open the CSV file in write mode
    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'date', 'score', 'sentiment'])

        file_is_empty = file.tell() == 0
        if file_is_empty:
            writer.writeheader()

        writer.writerows(data)