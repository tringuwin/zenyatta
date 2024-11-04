
from common_messages import invalid_number_of_params
from helpers import get_constant_value, valid_number_of_params
from datetime import datetime, timedelta


async def make_sol_week(db, message):
    
    valid_params, params = valid_number_of_params(message, 4)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    day = int(params[1])
    month = int(params[2])
    year = int(params[3])

    # todo

    league_season = 5 #get_constant_value(db, 'league_season')

    schedule_db = db['schedule']
    this_season_schedule = schedule_db.find_one({'season': league_season})
    weeks_in_season = len(this_season_schedule['weeks'])
    
    start_date = datetime(year, month, day)
    days_obj = []

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        
        day_of_week = current_date.strftime("%A")

        today_obj = {
            'date': day_of_week,
            'matches': [],
        }

    new_week_obj = {
        'week': weeks_in_season + 1,
        'days': days_obj
    }

    this_season_schedule['weeks'].append(new_week_obj)

    schedule_db.update_one({'season': league_season}, {'$set': {'weeks': this_season_schedule['weeks']}})

    await message.channel.send('Added week to league season')
