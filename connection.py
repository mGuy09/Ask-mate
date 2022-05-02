import csv


def read_question(data_csv):
    list_of_samples = []
    with open(data_csv, 'r') as file:
        read_csv = csv.DictReader(file)
        for row in read_csv:
            list_of_samples.append(row)
        return list_of_samples


def get_new_id(data_csv):
    return max([int(entry.get("id", 0)) for entry in read_question(data_csv)]) + 1


def append_question(data_csv, data):
    with open(data_csv, "a") as file:
        writer = csv.DictWriter(file)
        writer.writerow(data)