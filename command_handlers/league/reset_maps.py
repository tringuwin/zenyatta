
import constants
from safe_send import safe_send

async def reset_maps_handler(db, message):

    no_map = constants.NO_MAP_IMAGE

    blank_maps = {
        'map1': no_map,
        'map2': no_map,
        'map3': no_map,
        'map4': no_map,
        'map5': no_map,
        'map6': no_map,
        'map7': no_map
    }

    maps = db['maps']
    maps.update_one({"maps_id": 1}, {"$set": {"maps": blank_maps}})

    no_map_name = constants.NO_MAP_NAME

    blank_map_names = {
        'map1': no_map_name,
        'map2': no_map_name,
        'map3': no_map_name,
        'map4': no_map_name,
        'map5': no_map_name,
        'map6': no_map_name,
        'map7': no_map_name
    }

    map_names = db['mapnames']
    map_names.update_one({"maps_id": 1}, {"$set": {"maps": blank_map_names}})

    await safe_send(message.channel, 'Maps reset')