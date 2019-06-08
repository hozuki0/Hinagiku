import time
import datetime


def is_friday():
    return datetime.date.today().weekday() == 4
