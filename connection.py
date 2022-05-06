import csv


DATA_HEADER = [
    "id",
    "submission_time",
    "view_number",
    "vote_number",
    "title",
    "message",
    "image",
]
answer_header = [
    "id",
    "submission_time",
    "vote_number",
    "question_id",
    "message",
    "image",
]


def read_question(data_csv):
    with open(data_csv, "r") as file:
        read_csv = csv.DictReader(file)
        return list(read_csv)


def get_new_id(data_csv):
    data = read_question(data_csv)
    if len(data) == 0:
        return 1
    return max([int(entry.get("id", 0)) for entry in data]) + 1


def append_to_file(file, data, headers):
    with open(file, "a") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(data)


def append_data(data_csv, data):
    append_to_file(data_csv, data, DATA_HEADER)


def append_answer(data_csv, data):
    append_to_file(data_csv, data, answer_header)


def rewrite_file(filename, data, headers):
    with open(filename, "w") as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def delete_question(data_csv, question_list):
    rewrite_file(data_csv, question_list, DATA_HEADER)


def delete_answer(data_csv, answer_list):
    rewrite_file(data_csv, answer_list, answer_header)


def rewrite_question_data(data_csv, question_list):
    rewrite_file(data_csv, question_list, DATA_HEADER)


def rewrite_answer_data(data_csv, answer_list):
    rewrite_file(data_csv, answer_list, answer_header)
