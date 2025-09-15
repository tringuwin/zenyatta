

from automation.schedule_plan.make_schedule_plan import build_week_for_season
from command_handlers.league.swiss_matchups import convert_pairings_into_matchups
from safe_send import safe_reply, safe_send
from time_helpers import year_month_day_to_datetime


# ADD_WEEK_CONFIG = {

#     'start_day_info': {
#         'day': 12,
#         'month': 5,
#         'year': 2025
#     },
#     'season': 6,
#     'match_pairs': [
#         ['Deadlock', 'Hunters'],
#         ['Phoenix', 'Angels'],
#     ]

# }

ADD_WEEK_CONFIG = {

    'start_day_info': {
        'day': 15,
        'month': 9,
        'year': 2025
    },
    'season': 1,
    'match_pairs': [
        ['Saviors', 'Ragu'],
    ]

}

def get_all_teams_participating():

    all_teams = []

    for team in ADD_WEEK_CONFIG['match_pairs']:
        all_teams.append(team[0])
        all_teams.append(team[1])

    return all_teams


def make_schedule_week_from_schedule_plan_week(schedule_plan_week, week_num):

    schedule_week_days = []

    for day in schedule_plan_week['days']:
        schedule_week_date = day['date']

        schedule_week_days.append({
            'date': {
                'day': schedule_week_date['day'],
                'month': schedule_week_date['month'],
                'year': schedule_week_date['year'],
            },
            'day_of_week': day['day_of_week'],
            'matches': [],
        })

    new_schedule_week = {
        'week_num': week_num,
        'days': schedule_week_days
    }

    return new_schedule_week

async def add_week(db, message, context):

    schedule_plans = db['schedule_plans']
    schedule_plan = schedule_plans.find_one({'season': ADD_WEEK_CONFIG['season'], 'context': context})
    if not schedule_plan:
        await safe_reply(message, "No schedule plan found for the given season and context.")
        return
    
    schedules = db['schedule']
    schedule = schedules.find_one({'season': ADD_WEEK_CONFIG['season'], 'context': context})
    if not schedule:
        await safe_reply(message, "No schedule found for the given season and context.")
        return
    
    config_day_info = ADD_WEEK_CONFIG['start_day_info']
    schedule_week_start_datetime = year_month_day_to_datetime(config_day_info['year'], config_day_info['month'], config_day_info['day'])

    new_schedule_plan_week = build_week_for_season(schedule_week_start_datetime)

    # override alerts to not annoy teams
    new_schedule_plan_week['notifs']['notified_1_day_left'] = True
    new_schedule_plan_week['notifs']['notified_5_hours_left'] = True
    new_schedule_plan_week['notifs']['notified_1_hour_left'] = True

    new_schedule_plan_week['status'] = 'SCHEDULING'

    all_teams_participating = get_all_teams_participating()
    new_schedule_plan_week['teams_playing'] = all_teams_participating

    schedule_plan['weeks'].append(new_schedule_plan_week)

    # add matchups to db
    convert_pairings_into_matchups(db, ADD_WEEK_CONFIG['match_pairs'], schedule_plan)

    
    schedule_plans.update_one({'season': ADD_WEEK_CONFIG['season'], 'context': context}, {'$set': {'weeks': schedule_plan['weeks']}})

    new_schedule_week = make_schedule_week_from_schedule_plan_week(new_schedule_plan_week, len(schedule['weeks']) + 1)
    schedule['weeks'].append(new_schedule_week)
    schedules.update_one({'season': ADD_WEEK_CONFIG['season'], 'context': context}, {'$set': {'weeks': schedule['weeks']}})

    await safe_send(message.channel, 'additional week added')


