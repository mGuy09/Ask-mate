import datetime


def convert_time(time_in_millis):
    dt = datetime.datetime.fromtimestamp(time_in_millis / 1000.0)
    return dt
