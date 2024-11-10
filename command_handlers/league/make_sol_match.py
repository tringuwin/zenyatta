
import constants
from command_handlers.bets.new_bet import new_bet
from common_messages import invalid_number_of_params
from discord_actions import get_guild
from helpers import valid_number_of_params


TIMESLOT_TO_INFO = {

    'W-6': ['Wednesday', 6],
    'W-7': ['Wednesday', 7],
    'W-8': ['Wednesday', 8],
    'W-9': ['Wednesday', 9],
    'W-10': ['Wednesday', 10],

    'T-6': ['Thursday', 6],
    'T-7': ['Thursday', 7],
    'T-8': ['Thursday', 8],
    'T-9': ['Thursday', 9],
    'T-10': ['Thursday', 10],

    'F-6': ['Friday', 6],
    'F-7': ['Friday', 7],
    'F-8': ['Friday', 8],
    'F-9': ['Friday', 9],
    'F-10': ['Friday', 10],

    'S-2': ['Saturday', 2],
    'S-3': ['Saturday', 3],
    'S-4': ['Saturday', 4],
    'S-5': ['Saturday', 5],
    'S-6': ['Saturday', 6],
    'S-7': ['Saturday', 7],
    'S-8': ['Saturday', 8],
    'S-9': ['Saturday', 9],
    'S-10': ['Saturday', 10],

    'X-2': ['Sunday', 2],
    'X-3': ['Sunday', 3],
    'X-4': ['Sunday', 4],
    'X-5': ['Sunday', 5],
    'X-6': ['Sunday', 6],
    'X-7': ['Sunday', 7],
    'X-8': ['Sunday', 8],
    'X-9': ['Sunday', 9],
    'X-10': ['Sunday', 10],

}

def get_weekday_index(week_data, match_weekday):

    cur_day_index = 0

    while True:
        if week_data['days'][cur_day_index]['weekday'] == match_weekday:
            return cur_day_index
        
        cur_day_index += 1


def sort_matches_by_time(matches):

    sorted_matches = sorted(matches, key=lambda obj: obj['raw_time'])
    return sorted_matches


async def make_sol_match(client, db, message):

    valid_params, params = valid_number_of_params(message, 5)

    if not valid_params:
        await invalid_number_of_params(message)
        return

    week_num = int(params[1])
    team_1 = params[2].lower()
    team_2 = params[3].lower()
    timeslot = params[4].upper()

    if not (timeslot in TIMESLOT_TO_INFO):
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

    league_season = 5 #get_constant_value(db, 'league_season')

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

    timeslot_info = TIMESLOT_TO_INFO[timeslot]
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
        'raw_time': match_start_est
    }

    day_data['matches'].append(match_obj)

    sorted_matches = sort_matches_by_time(day_data['matches'])
    day_data['matches'] = sorted_matches
    week_data['days'][weekday_index] = day_data
    league_schedule['weeks'][week_index] = week_data

    schedules.update_one({'season': league_season}, {'$set': {'weeks': league_schedule['weeks']}})

    guild = await get_guild(client)
    team_1_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_1_name]
    team_1_emoji = guild.get_emoji(team_1_emoji_id)
    team_2_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_2_name]
    team_2_emoji = guild.get_emoji(team_2_emoji_id)

    bet_title = 'WEEK '+str(week_num)+' : '+match_weekday.upper()+' : '+str(team_1_emoji)+' '+team_1_name+' VS '+str(team_2_emoji)+' '+team_2_name
    await new_bet(client, db, bet_title, team_1_name, team_2_name, True)

    await message.channel.send('Match added successfully')






