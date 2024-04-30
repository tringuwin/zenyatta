

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
import constants


ALL_LEVELS = {


    '1': {
        
    }


}




async def server_points_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    num_points = params[1]
    if not can_be_int(num_points):
        await message.channel.send(num_points+' is not a number')
        return
    
    num_points = int(num_points)
    orig_points = num_points
    level = 0
    while num_points > 5000:
        num_points -= 5000
        level += 1

    constants_db = db['constants']
    server_level_obj = constants_db.find_one({'name': 'server_level'})
    server_level = server_level_obj['value']['level']

    points_to_next_level = 5000 - num_points

    server_level_channel = client.get_channel(constants.SERVER_LEVEL_CHANNEL)
    level_message = await server_level_channel.fetch_message(constants.SERVER_LEVEL_MESSAGE)

    level_string = 'CURRENT SERVER LEVEL: **'+str(level)+'**'
    level_string += '\nCURRENT SERVER POINTS: **'+format(orig_points, ',')+'**'
    level_string += '\nPOINTS TO NEXT LEVEL: **'+format(points_to_next_level, ',')+'**'
    level_string += '\n-----------------------------------'
    level_string += '\nSERVER STATS:'
    level_string += '\nToken Shop Stock Added Per Week: ERROR'
    level_string += '\nSOL Prize Money Added Per Week: ERROR'
    level_string += '\nDaily Auction Prizes Tier: ERROR'
    level_string += '\n-----------------------------------'
    level_string += '\nCurrent SOL Prize Pool'
    level_string += '\n-----------------------------------'

    await level_message.edit(content=level_string)

    if server_level != level:
        pass
    
    await message.channel.send('level: '+str(level)+' - points: '+str(num_points))

    

    

