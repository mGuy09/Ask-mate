
import datetime


def convert_time(time_in_millis):
    dt = datetime.datetime.fromtimestamp(float(time_in_millis) / 1000.0,)
    dt = dt.strftime('%d/%m/%Y  %H:%M')
    return dt


def convert_to_hours(time_in_millis):
    dt = datetime.datetime.fromtimestamp(float(time_in_millis) / 1000.0,)
    dt = dt.strftime('%H:%M')
    return dt
