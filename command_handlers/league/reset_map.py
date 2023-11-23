

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params

import constants

async def reset_map_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    map_num = params[1]
    if not can_be_int(map_num):
        await message.channel.send(map_num+' is not a valid integer')
        return

    map_num = int(map_num)
    if map_num > 7 or map_num < 1:
        await message.channel.send('Map num must be between 1 and 7')
        return
    
    maps = db['maps']
    map_group = maps.find_one({'maps_id': 1})
    map_group['maps']['map'+str(map_num)] = constants.NO_MAP_IMAGE

    maps.update_one({"maps_id": 1}, {"$set": {"maps": map_group['maps']}})

    await message.channel.send('Map '+str(map_num)+' reset')