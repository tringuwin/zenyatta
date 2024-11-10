
from common_messages import invalid_number_of_params
from helpers import get_constant_value, valid_number_of_params
from datetime import datetime, timedelta


def get_day_with_suffix(day):
    if 10 <= day % 100 <= 20:  # Special case for '11th', '12th', '13th', etc.
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return f"{day}{suffix}"

async def make_sol_week(db, message):
    
    valid_params, params = valid_number_of_params(message, 4)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    day = int(params[1])
    month = int(params[2])
    year = int(params[3])

    league_season = 5 #get_constant_value(db, 'league_season')

    schedule_db = db['schedule']
    this_season_schedule = schedule_db.find_one({'season': league_season})
    weeks_in_season = len(this_season_schedule['weeks'])
    
    start_date = datetime(year, month, day)
    days_obj = []

    for i in range(7):
        current_date = start_date + timedelta(days=i)
        
        day_of_week = current_date.strftime("%A")
        month_name = current_date.strftime("%B")
        day_num = int(current_date.strftime("%d"))
        month_num = int(current_date.strftime("%m"))
        year_num = int(current_date.strftime("%Y"))
        day_with_suffix = get_day_with_suffix(day_num)

        today_obj = {
            'date': f'{day_of_week}, {month_name} {day_with_suffix}',
            'start_time': 'TBD',
            'matches': [],
            'day_data': {
                'day': day_num,
                'month': month_num,
                'year': year_num
            },
            'weekday': day_of_week
        }

        days_obj.append(today_obj)

    new_week_obj = {
        'week': weeks_in_season + 1,
        'days': days_obj
    }

    this_season_schedule['weeks'].append(new_week_obj)

    schedule_db.update_one({'season': league_season}, {'$set': {'weeks': this_season_schedule['weeks']}})

    await message.channel.send('Added week to league season')
