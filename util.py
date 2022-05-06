from datetime import datetime


def convert_time(time_in_millis):
    dt = datetime.fromtimestamp(
        float(time_in_millis) / 1000.0,
    )
    dt = dt.strftime("%d/%m/%Y  %H:%M")
    return dt


def get_time():
    now = datetime.now()
    now = now.strftime("%d/%m/%Y %H:%M:%S:%fff")
    now = datetime.strptime(now, "%d/%m/%Y %H:%M:%S:%fff")
    current_time = now.timestamp() * 1000
    return current_time
