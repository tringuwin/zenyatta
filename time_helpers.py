import time
import constants
from datetime import datetime
import pytz

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


def time_to_shop(diff_in_time):
    
    time_to_shop = constants.TIME_BETWEEN_SHOP - diff_in_time

    days = 0
    hours = 0
    minutes = 0

    while time_to_shop > 86400:
        days += 1
        time_to_shop -= 86400
    while time_to_shop > 3600:
        hours += 1
        time_to_shop -= 3600
    while time_to_shop >= 60:
        minutes += 1
        time_to_shop -= 60

    return format_time(days, 'days')+format_time(hours, 'hours')+format_time(minutes, 'minutes')+format_time(int(time_to_shop), 'seconds')


def get_current_time():

    current_time = int(time.time())
    return current_time

def long_enough_for_gift(last_gift):

    current_time = get_current_time()
    diff_in_time = current_time - last_gift

    if diff_in_time >= constants.TIME_BETWEEN_GIFTS:
        return True, diff_in_time
    else:
        return False, diff_in_time
    
def long_enough_for_shop(last_shop):

    current_time = get_current_time()
    diff_in_time = current_time - last_shop

    if diff_in_time >= constants.TIME_BETWEEN_SHOP:
        return True, diff_in_time
    else:
        return False, diff_in_time    
    

def get_current_day_est():
    # Get current time in UTC
    now_utc = datetime.utcnow()

    # Convert UTC time to EST
    est = pytz.timezone('US/Eastern')
    now_est = now_utc.replace(tzinfo=pytz.utc).astimezone(est)

    # Get the day as an integer
    day = now_est.day

    return day