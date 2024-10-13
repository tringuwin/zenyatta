import time
import constants
from datetime import datetime
import pytz

from discord_actions import get_guild
from helpers import get_constant_value
from server_level import level_to_prize_money, level_to_token_shop_cash
from shop import update_shop

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



def been_a_week(db):

    cur_tick = time.time()

    constants_db = db['constants']
    week_obj = constants_db.find_one({'name': 'week_tick'})
    week_tick = week_obj['value']

    if cur_tick - week_tick > constants.SECONDS_IN_A_WEEK:
        constants_db.update_one({"name": 'week_tick'}, {"$set": {"value": int(week_tick + constants.SECONDS_IN_A_WEEK)}})
        return True
    
    return False



async def check_weekly(client, db, channel, message):

    week_passed = been_a_week(db)

    if not week_passed:
        await channel.send('Has not been a week for prize money constant')
        return
    
    # get the full amount of money
    funding = get_constant_value(db, 'funding')
    total_funding = funding['raw_funding']

    # subract expenses
    left_after_expenses = total_funding - funding['expenses']

    # subtract owner share
    left_after_share = left_after_expenses * funding['owner_percent']

    # divide among prize pools
    token_shop_funding = round(left_after_share * funding['percentages']['token_shop'], 2)
    daily_auction_funding = round(left_after_share * funding['percentages']['daily_auction'], 2)
    prize_money = round(left_after_share * funding['percentages']['prize_money'], 2)
    
    constants_db = db['constants']
    server_level_obj = constants_db.find_one({'name': 'server_level'})
    server_level_num = server_level_obj['value']['level']

    new_money = level_to_prize_money(server_level_num)

    prize_money_obj = constants_db.find_one({'name': 'prize_money'})
    old_money = prize_money_obj['value']

    constants_db.update_one({"name": 'prize_money'}, {"$set": {"value": int(new_money+old_money)}})

    await channel.send('Prize money added to total!')

    # token shop refill

    # get weekly token shop cash
    token_shop_cash = 12.30 #level_to_token_shop_cash(server_level_num)

    # edit prices
    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 2})
    items = the_shop['offers']
    for offer in items:

        if offer['in_stock'] == 0:
            offer['price'] += 100
        else:
            offer['price'] -= 100

    # always set pokepoints to 800
    items[6]['price'] = 800

    # distribute goods
    increase_array = [0, 0, 0, 0, 0, 0, 0]
    increase_index = 0
    token_shop_cash -= 5
    while token_shop_cash > 0:
        increase_array[increase_index] += 1
        token_shop_cash -= constants.TOKEN_SHOP_USD_PRICES[increase_index]
        increase_index += 1
        if increase_index == len(increase_array):
            increase_index = 0

    i = 0
    while i < len(increase_array):
        items[i]['in_stock'] += increase_array[i]
        i += 1

    # update shop
    shop.update_one({"shop_id": 2}, {"$set": {"offers": items}})
    await update_shop(db, message)

    # set last token shop for each user
    users = db['users']
    all_users = users.find()
    for user in all_users:

        if 'last_token_shop' in user:
            users.update_one({"discord_id": user['discord_id']}, {"$set": {"last_token_shop": 0}})

    # confirmation message
    await channel.send('Successfully re-stocked token shop!')

    guild = await get_guild(client)
    announcements_channel = guild.get_channel(constants.ANNOUNCEMENTS_CHANNEL_ID)
    await announcements_channel.send('<@&1246634634259857459> THE TOKEN SHOP HAS BEEN RE-STOCKED! <#1187062494561325056>')


