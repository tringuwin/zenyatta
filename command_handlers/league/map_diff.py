

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params

import constants

async def map_diff_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)

    if not valid_params:
        await invalid_number_of_params(message)
        return

    team_name = params[1]
    if not team_name in constants.TEAM_LIST:
        await message.channel.send(team_name+' is not a valid team name')
        return
    
    num_to_add = params[2]
    if not can_be_int(num_to_add):
        await message.channel.send(params[2]+' is not a number')
        return
    num_to_add = int(num_to_add)
    
    standings = db['standings']
    standings_obj = standings.find_one({'season': constants.LEAGUE_SEASON})
    standings_obj['teams'][team_name][2] += num_to_add

    standings.update_one({"season": constants.LEAGUE_SEASON}, {"$set": {"teams": standings_obj['teams']}})

    await message.channel.send('team maps changed')