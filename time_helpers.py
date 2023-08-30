import time
import constants

def format_time(num, title):

    if num == 0:
        return ''

    return str(num)+' '+title+' '


def time_to_gift(diff_in_time):

    time_to_gift = constants.TIME_BETWEEN_GIFTS - diff_in_time

    hours = 0
    minutes = 0

    while time_to_gift > 3600:
        hours += 1
        time_to_gift -= 3600
    while time_to_gift >= 60:
        minutes += 1
        time_to_gift -= 60

    return format_time(hours, 'hours')+format_time(minutes, 'minutes')+format_time(time_to_gift, 'seconds')

def get_current_time():

    current_time = int(time.time())
    return current_time

def long_enough_for_gift(user):

    current_time = get_current_time()
    diff_in_time = current_time - user['last_gift']

    if diff_in_time >= constants.TIME_BETWEEN_GIFTS:
        return True, diff_in_time
    else:
        return False, diff_in_time