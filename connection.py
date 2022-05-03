import csv

import data_manager

DATA_HEADER = ['id','submission_time','view_number','vote_number','title','message','image']
answer_header = ['id','submission_time','vote_number','question_id','message','image']

def read_question(data_csv):
    list_of_samples = []
    with open(data_csv, 'r') as file:
        read_csv = csv.DictReader(file)
        for row in read_csv:
            list_of_samples.append(row)
        return list_of_samples


def get_new_id(data_csv):
    return max([int(entry.get("id", 0)) for entry in read_question(data_csv)]) + 1


def append_data(data_csv, data):
    with open(data_csv, "a") as file:
        writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        writer.writerow(data)


def append_answer(data_csv, data):
    with open(data_csv, "a") as file:
        writer = csv.DictWriter(file, fieldnames=answer_header)
        writer.writerow(data)


def delete_question(data_csv, question_list):
    with open(data_csv, "w") as file:
        writer = csv.DictWriter(file, fieldnames=DATA_HEADER)
        writer.writeheader()
        for row in question_list:
            writer.writerow(row)



