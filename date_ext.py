import time
import datetime


def is_friday():
    return datetime.date.today().weekday() == 4


def is_friday_night():
    return is_friday() and datetime.now().hour > 20
