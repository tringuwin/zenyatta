

from automation.schedule_plan.make_schedule_plan import build_week_for_season
from time_helpers import year_month_day_to_datetime


ADD_WEEK_CONFIG = {

    'start_day_info': {
        'day': 28,
        'month': 4,
        'year': 2025
    },
    'season': 6,
    'match_pairs': [
        ['Horizon', 'Ragu'],
        ['Angels', 'Polar'],
        ['Lotus', 'Instigators'],
        ['Saturn', 'Deadlock']
    ]

}

async def add_week(db, message, context):

    schedule_plans = db['schedule_plans']
    schedule_plan = schedule_plans.find_one({'season': ADD_WEEK_CONFIG['season'], 'context': context})
    if not schedule_plan:
        await message.reply("No schedule plan found for the given season and context.")
        return
    
    config_day_info = ADD_WEEK_CONFIG['start_day_info']
    schedule_week_start_datetime = year_month_day_to_datetime(config_day_info['year'], config_day_info['month'], config_day_info['day'])

    new_schedule_week = build_week_for_season(schedule_week_start_datetime)

    # override alerts to not annoy teams
    new_schedule_week['notifs']['notified_1_day_left'] = True
    new_schedule_week['notifs']['notified_5_hours_left'] = True
    new_schedule_week['notifs']['notified_1_hour_left'] = True

    schedule_plan['weeks'].append(new_schedule_week)

    schedule_plans.update_one({'season': ADD_WEEK_CONFIG['season'], 'context': context}, {'$set': {'weeks': schedule_plan['weeks']}})

    await message.channel.send('additional week added')


