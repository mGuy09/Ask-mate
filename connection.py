import csv


def read_question(data_csv):
    list_of_samples = []
    with open(data_csv, 'r') as file:
        read_csv = csv.DictReader(file)
        for row in read_csv:
            list_of_samples.append(row)

    return list_of_samples
