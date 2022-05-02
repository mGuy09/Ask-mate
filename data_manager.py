import connection


def get_data(csv_file):
    csv_data = connection.read_question(csv_file)
    return csv_data
