
import constants

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

    await message.channel.send('Maps reset')