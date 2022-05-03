import connection
import util


def get_data(csv_file):
    csv_data = connection.read_question(csv_file)
    return csv_data


def sort_asc(csv_file, order_value, order_direction):
    csv_data = get_data(csv_file)
    csv_data = sorted(csv_data, key=lambda row: row[order_value], reverse=(order_direction == 'asc'))

    for i in csv_data:
        i['submission_time'] = util.convert_time(i['submission_time'])

    if order_value == 'view_number':
        csv_data = sorted(csv_data, key=lambda row: int(row[order_value]), reverse=(order_direction == 'desc'))

    if order_value == 'vote_number':
        csv_data = sorted(csv_data, key=lambda row: int(row[order_value]), reverse=(order_direction == 'desc'))
    return csv_data


def remove_question(data_csv, id):
    question_list = connection.read_question(data_csv)

    for i in question_list:
        if i["id"] == id:
            deleted_question = i
    question_list.remove(deleted_question)
    connection.delete_question(data_csv, question_list)


def remove_answer(data_csv, id):
    answer_list = connection.read_question(data_csv)

    for i in answer_list:
        if i["id"] == id:
            deleted_answer = i
    question_id = deleted_answer["question_id"]
    answer_list.remove(deleted_answer)
    connection.delete_answer(data_csv, answer_list)
    return question_id


