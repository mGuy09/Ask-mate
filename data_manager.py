import connection
import operator

def get_data(csv_file):
    csv_data = connection.read_question(csv_file)
    return csv_data


def sort_asc(csv_file, order_value, order_direction):
    csv_data = get_data(csv_file)
    csv_data = sorted(csv_data, key=operator.itemgetter(order_value), reverse=order_direction)
    return csv_data

