
from common_messages import invalid_number_of_params
from helpers import get_constant_value, valid_number_of_params

import constants
from safe_send import safe_send

async def add_loss_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name_lower = params[1].lower()
    league_teams = db['leagueteams']
    my_team = league_teams.find_one({'name_lower': team_name_lower})
    if not my_team:
        await safe_send(message.channel, params[1]+' is not a valid team name')
        return
    team_name = my_team['team_name']

    league_season = get_constant_value(db, 'league_season')
    
    standings = db['standings']
    standings_obj = standings.find_one({'season': league_season})
    standings_obj['teams'][team_name][1] += 1

    standings.update_one({"season": league_season}, {"$set": {"teams": standings_obj['teams']}})

    await safe_send(message.channel, 'team loss added')