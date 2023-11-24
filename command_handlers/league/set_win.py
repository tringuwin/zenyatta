

from common_messages import invalid_number_of_params
from helpers import can_be_int, make_string_from_word_list

import constants

async def set_win_handler(db, message):

    word_parts = message.content.split()
    if len(word_parts) < 3:
        await invalid_number_of_params(message)
        return
    
    team_name = make_string_from_word_list(word_parts, 2)
    if not team_name in constants.TEAM_LIST:
        await message.channel.send(team_name+' is not a valid team name')
        return
    
    map_num = word_parts[1]
    if not can_be_int(map_num):
        await message.channel.send(map_num+' is not an integer')
        return
    
    map_num = int(map_num)
    if map_num > 7 or map_num < 1:
        await message.channel.send('Map num must be beween 1 and 7')
        return
    
    local_files = db['localfiles']
    files = local_files.find_one({'files_id': 1})

    files['files']['map_wins']['data']['map'+str(map_num)] = team_name
    files['files']['map_wins']['version'] += 1

    local_files.update_one({"files_id": 1}, {"$set": {"files": files['files']}})

    await message.channel.send('Map winner set')
