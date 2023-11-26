

from common_messages import invalid_number_of_params
from helpers import make_string_from_word_list

import constants

async def add_win_handler(db, message):

    word_parts = message.content.split()
    if len(word_parts) < 2:
        await invalid_number_of_params(message)
        return
    
    team_name = make_string_from_word_list(word_parts, 1)
    if not team_name in constants.TEAM_LIST:
        await message.channel.send(team_name+' is not a valid team name')
        return
    
    standings = db['standings']
    standings_obj = standings.find_one({'season': constants.LEAGUE_SEASON})
    standings_obj['teams'][team_name][0] += 1

    standings.update_one({"season": constants.LEAGUE_SEASON}, {"$set": {"teams": standings_obj['teams']}})

    await message.channel.send('team win added')