

from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from helpers import can_be_int, valid_number_of_params
from time_helpers import get_day_info_for_future_day, get_future_week_datetime, year_month_day_to_datetime


def get_schedule_plan_with_season_and_context(schedule_plans, season, context):

    existing_schedule_plan = schedule_plans.find_one({'season': season, 'context': context})
    return existing_schedule_plan

    
def get_teams_for_season(db, context, blacklist):

    league_teams_collection = get_league_teams_collection_from_context(db, context)
    season_teams = league_teams_collection.find()

    teams_for_season = []

    for team in season_teams:
        if not team['team_name'] in blacklist:
            teams_for_season.append(
                {
                    'team_name': team['team_name'],
                    'teams_played': [],
                    'invisible_elo': -1
                }
            )

    return teams_for_season


def is_match_day(day_of_week):

    if day_of_week == 'Monday' or day_of_week == 'Tuesday':
        return False
    
    return True


def build_days_for_week(season_week_datetime):

    days = []

    for i in range(7):
        day_info = get_day_info_for_future_day(season_week_datetime, i)

        days.append({
            'status': 'NOT STARTED',
            'date': day_info['date'],
            'day_of_week': day_info['day_of_week'],
            'is_match_day': is_match_day(day_info['day_of_week']),
            'notified': False,
            'set_up_casting': False
        })

    return days


def build_week_for_season(season_week_datetime):

    new_week = {
        'status': 'NOT STARTED',
        'day_number': 0,
        'days': build_days_for_week(season_week_datetime),
        'notifs': {
            'notified_1_day_left': False,
            'notified_5_hours_left': False,
            'notified_1_hour_left': False,
        }
    }

    return new_week


def build_weeks_for_season(day, month, year, num_weeks_in_season):

    weeks = []

    start_datetime = year_month_day_to_datetime(year, month, day)

    for i in range(num_weeks_in_season):

        season_week_datetime = get_future_week_datetime(start_datetime, i)
        new_week = build_week_for_season(season_week_datetime)
        weeks.append(new_week)

    return weeks


def make_standings_for_season(context, season_number, teams_for_season):

    team_names = []
    for team in teams_for_season:
        team_names.append(team['team_name'])

    standings_teams = {}
    for team_name in team_names:
        standings_teams[team_name] = {
            'team_name': team_name,
            'wins': 0,
            'losses': 0,
            'map_wins': 0,
            'map_losses': 0,
            'points': 0,
            'forfeits': 0,
        }

    return {
        'context': context,
        'season': season_number,
        'teams': standings_teams,
        'forfeits': {}
    }


def make_schedule_for_season(context, season_number, season_weeks):

    schedule_weeks = []

    week_index = 1
    for week in season_weeks:

        week_days = []
        for day in week['days']:
            week_days.append({
                'date': day['date'],
                'day_of_week': day['day_of_week'],
                'matches': [],
            })

        schedule_weeks.append({
            'week_num': week_index,
            'days': week_days
        })

        week_index += 1

    return {
        'context': context,
        'season': season_number,
        'weeks': schedule_weeks
    }


async def make_schedule_plan(message, db, context):

    valid_params, params = valid_number_of_params(message, 7)

    if not valid_params:
        await invalid_number_of_params(message)
        return

    season_number = params[1]
    if not can_be_int(season_number):
        await message.channel.send(season_number+' is not a valid season number.')
        return
    season_number = int(season_number)

    league_start_day = params[2]
    if not can_be_int(league_start_day):
        await message.channel.send(league_start_day+' is not a valid day.')
        return
    league_start_day = int(league_start_day)

    league_start_month = params[3]
    if not can_be_int(league_start_month):
        await message.channel.send(league_start_month+' is not a valid month.')
        return
    league_start_month = int(league_start_month)

    league_start_year = params[4]
    if not can_be_int(league_start_year):
        await message.channel.send(league_start_year+' is not a valid year.')
        return
    league_start_year = int(league_start_year)

    num_weeks_in_season = params[5]
    if not can_be_int(num_weeks_in_season):
        await message.channel.send(num_weeks_in_season+' is not a number.')
        return
    num_weeks_in_season = int(num_weeks_in_season)

    team_blacklist = params[6].split('|')

    schedule_plans = db['schedule_plans']
    existing_schedule_plan = get_schedule_plan_with_season_and_context(schedule_plans, season_number, context)
    if existing_schedule_plan:
        await message.channel.send(f'A Schedule Plan already exists with season number {season_number} for context {context}')
        return
    
    teams_for_season = get_teams_for_season(db, context, team_blacklist)
    if len(teams_for_season) % 2 != 0:
        await message.channel.send(f'There are an odd number of teams in the league. Cannot create schedule plan.')
        return

    new_schedule_plan = {
        'context': context,
        'season': season_number,
        'status': 'NOT STARTED',
        'weeks': build_weeks_for_season(league_start_day, league_start_month, league_start_year, num_weeks_in_season),
        'current_week': 0,
        'season_teams': teams_for_season,
        'matchups_config': {
            'auto_generate': False,
            'weeks_of_invisible_elo': 3
        }
    }
    schedule_plans.insert_one(new_schedule_plan)

    standings = db['standings']
    new_standings = make_standings_for_season(context, season_number, teams_for_season)
    standings.insert_one(new_standings)

    schedule_db = db['schedule']
    new_schedule = make_schedule_for_season(context, season_number, new_schedule_plan['weeks'])
    schedule_db.insert_one(new_schedule)

    await message.channel.send(f'Schedule Plan created for season number {season_number} for context {context}')
    
