

from common_messages import invalid_number_of_params
from helpers import can_be_int, get_constant_value, valid_number_of_params


async def match_end_handler(db, message):

    valid_params, params = valid_number_of_params(message, 5)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    win_score = params[2]
    lose_score = params[4]

    if not can_be_int(win_score):
        await message.channel.send(win_score+' is not a valid number.')
        return
    if not can_be_int(lose_score):
        await message.channel.send(lose_score+' is not a valid number.')
        return
    
    win_score = int(win_score)
    lose_score = int(lose_score)

    win_team_name = params[1]
    lose_team_name = params[3]

    win_team_name_lower = win_team_name.lower()
    lose_team_name_lower = lose_team_name.lower()
    league_teams = db['leagueteams']

    win_team = league_teams.find_one({'name_lower': win_team_name_lower})
    if not win_team:
        await message.channel.send(win_team_name+' is not a valid team name')
        return
    lose_team = league_teams.find_one({'name_lower': lose_team_name_lower})
    if not lose_team:
        await message.channel.send(lose_team_name+' is not a valid team name')
        return
    
    win_team_real_name = win_team['team_name']
    lose_team_real_name = lose_team['team_name']

    map_diff = win_score - lose_score

    league_season = get_constant_value(db, 'league_season')
    
    standings = db['standings']
    standings_obj = standings.find_one({'season': league_season})

    standings_obj['teams'][win_team_real_name][0] += 1
    standings_obj['teams'][win_team_real_name][2] += map_diff
    standings_obj['teams'][lose_team_real_name][1] += 1
    standings_obj['teams'][lose_team_real_name][2] -= map_diff

    standings.update_one({"season": league_season}, {"$set": {"teams": standings_obj['teams']}})

    await message.channel.send('match info recorded')