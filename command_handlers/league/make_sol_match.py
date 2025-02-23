
from datetime import datetime
import pytz
import constants
from command_handlers.bets.new_bet import new_bet
from common_messages import invalid_number_of_params
from helpers import get_constant_value, get_league_emoji_from_team_name, valid_number_of_params


def get_weekday_index(week_data, match_weekday):

    cur_day_index = 0

    while True:
        if week_data['days'][cur_day_index]['weekday'] == match_weekday:
            return cur_day_index
        
        cur_day_index += 1


def sort_matches_by_time(matches):

    sorted_matches = sorted(matches, key=lambda obj: obj['raw_time'])
    return sorted_matches


def calculate_tick_of_match(year, month, day, hour):

    hour_converted_to_pm = hour + 12

    est = pytz.timezone('US/Eastern')
    naive_datetime = datetime(year, month, day, hour_converted_to_pm, 0, 0)
    est_datetime = est.localize(naive_datetime, is_dst=None)

    timestamp_ms = int(est_datetime.timestamp())

    return timestamp_ms


async def make_sol_match(client, db, message):

    valid_params, params = valid_number_of_params(message, 5)

    if not valid_params:
        await invalid_number_of_params(message)
        return

    week_num = int(params[1])
    team_1 = params[2].lower()
    team_2 = params[3].lower()
    timeslot = params[4].upper()

    if not (timeslot in constants.TIMESLOT_TO_INFO):
        await message.channel.send('That is not a valid timeslot')
        return
    
    league_teams = db['leagueteams']

    team_1_obj = league_teams.find_one({'name_lower': team_1})
    if not team_1_obj:
        await message.channel.send('Could not find team '+team_1)
        return
    team_1_name = team_1_obj['team_name']
    
    team_2_obj = league_teams.find_one({'name_lower': team_2})
    if not team_2_obj:
        await message.channel.send('Could not find team '+team_2)
        return
    team_2_name = team_2_obj['team_name']

    league_season = get_constant_value(db, 'league_season')

    schedules = db['schedule']

    league_schedule = schedules.find_one({'season': league_season})
    if not league_schedule:
        await message.channel.send('There is not a schedule for the current league season')
        return
    
    if len(league_schedule['weeks']) < week_num:
        await message.channel.send('That week number is too high')
        return
    
    if week_num < 1:
        await message.channel.send('That week number is too low')
        return
    
    week_index = week_num - 1
    week_data = league_schedule['weeks'][week_index]

    timeslot_info = constants.TIMESLOT_TO_INFO[timeslot]
    match_weekday = timeslot_info[0]
    match_start_est = timeslot_info[1]

    weekday_index = get_weekday_index(week_data, match_weekday)
    day_data = week_data['days'][weekday_index]

    # handle start time stuff
    replace_start_time = False
    start_time = day_data['start_time']
    if start_time == 'TBD':
        replace_start_time = True
    else:
        raw_start = int(start_time.split(':')[0])
        if raw_start > match_start_est:
            replace_start_time = True

    if replace_start_time:
        day_data['start_time'] = str(match_start_est)+':00'

    # create match object and insert
    match_obj = {
        'home': team_1_name,
        'away': team_2_name,
        'time': str(match_start_est)+' PM',
        'raw_time': match_start_est,
        'home_score': 0,
        'away_score': 0,
        'left_team': 'home'
    }

    day_data['matches'].append(match_obj)

    sorted_matches = sort_matches_by_time(day_data['matches'])
    day_data['matches'] = sorted_matches
    week_data['days'][weekday_index] = day_data
    league_schedule['weeks'][week_index] = week_data

    schedules.update_one({'season': league_season}, {'$set': {'weeks': league_schedule['weeks']}})

    team_1_emoji_string = get_league_emoji_from_team_name(team_1_name)
    team_2_emoji_string = get_league_emoji_from_team_name(team_2_name)

    bet_title = 'WEEK '+str(week_num)+' : '+match_weekday.upper()+' : '+team_1_emoji_string+' '+team_1_name+' VS '+team_2_emoji_string+' '+team_2_name
    match_day_numbers = day_data['day_data']
    timestamp_of_match = calculate_tick_of_match(match_day_numbers['year'], match_day_numbers['month'], match_day_numbers['day'], match_start_est)
    await new_bet(client, db, bet_title, team_1_name, team_2_name, False, timestamp_of_match)

    await message.channel.send('Match added successfully')






