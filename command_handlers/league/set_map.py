

from common_messages import invalid_number_of_params
from helpers import can_be_int
import constants

async def set_map_handler(db, message):

    parts = message.content.split('|')
    if len(parts) != 3:
        await invalid_number_of_params(message)
        return
    
    map_num = parts[1]
    if not can_be_int(map_num):
        await message.channel.send(map_num+' is not a valid integer')
        return
    
    map_num = int(map_num)
    if map_num > 7 or map_num < 1:
        await message.channel.send('Map num must be between 1 and 7')
        return

    map_name = parts[2]
    if not map_name in constants.MAP_NAME_TO_IMAGE:
        await message.channel.send(map_name+' is not a valid map name')
        return
    
    maps = db['maps']
    map_group = maps.find_one({'maps_id': 1})
    map_group['maps']['map'+str(map_num)] = constants.MAP_NAME_TO_IMAGE[map_name]
    maps.update_one({"maps_id": 1}, {"$set": {"maps": map_group['maps']}})

    map_names = db['mapnames']
    map_name_group = map_names.find_one({'maps_id': 1})
    map_name_group['maps']['map'+str(map_num)] = constants.MAP_NAME_TO_NAME_IMG[map_name]
    map_names.update_one({"maps_id": 1}, {"$set": {"maps": map_name_group['maps']}})

    await message.channel.send('Map updated')