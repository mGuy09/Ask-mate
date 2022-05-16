# import csv
#
#
# DATA_HEADER = [
#     "id",
#     "submission_time",
#     "view_number",
#     "vote_number",
#     "title",
#     "message",
#     "image",
# ]
# answer_header = [
#     "id",
#     "submission_time",
#     "vote_number",
#     "question_id",
#     "message",
#     "image",
# ]
#
#
# def read_question(data_csv):
#     with open(data_csv, "r") as file:
#         read_csv = csv.DictReader(file)
#         return list(read_csv)
#
#
# def get_new_id(data_csv):
#     data = read_question(data_csv)
#     if len(data) == 0:
#         return 1
#     return max([int(entry.get("id", 0)) for entry in data]) + 1
#
#
# def append_to_file(file, data, headers):
#     with open(file, "a") as f:
#         writer = csv.DictWriter(f, fieldnames=headers)
#         writer.writerow(data)
#
#
# def append_data(data_csv, data):
#     append_to_file(data_csv, data, DATA_HEADER)
#
#
# def append_answer(data_csv, data):
#     append_to_file(data_csv, data, answer_header)
#
#
# def rewrite_file(filename, data, headers):
#     with open(filename, "w") as file:
#         writer = csv.DictWriter(file, fieldnames=headers)
#         writer.writeheader()
#         for row in data:
#             writer.writerow(row)
#
#
# def delete_question(data_csv, question_list):
#     rewrite_file(data_csv, question_list, DATA_HEADER)
#
#
# def delete_answer(data_csv, answer_list):
#     rewrite_file(data_csv, answer_list, answer_header)
#
#
# def rewrite_question_data(data_csv, question_list):
#     rewrite_file(data_csv, question_list, DATA_HEADER)
#
#
# def rewrite_answer_data(data_csv, answer_list):
#     rewrite_file(data_csv, answer_list, answer_header)


def get_connection_string():
    # setup connection string
    # to do this, please define these environment variables first
    os.environ['PSQL_USER_NAME'] = 'postgres'
    os.environ['PSQL_PASSWORD'] = 'postgres'
    os.environ['PSQL_HOST'] = 'localhost'
    os.environ['PSQL_DB_NAME'] = 'sample_data'


    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        # this string describes all info for psycopg2 to connect to the database
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = get_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper