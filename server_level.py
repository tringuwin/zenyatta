

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
import constants


ALL_LEVELS = {


    '1': {
        'info': '',
        'token_shop': 50,
        'prize_money': 0,
        'auction': 0,
    },
    '2': {
        'info': '',
        'token_shop': 50,
        'prize_money': 0,
        'auction': 1,
    },
    '3': {
        'info': '',
        'token_shop': 75,
        'prize_money': 0,
        'auction': 1,
    },
    '4': {
        'info': '',
        'token_shop': 100,
        'prize_money': 0,
        'auction': 1,
    },
    '5': {
        'info': '',
        'token_shop': 100,
        'prize_money': 5,
        'auction': 1,
    },
    '6': {
        'info': '',
        'token_shop': 100,
        'prize_money': 5,
        'auction': 2,
    },
    '7': {
        'info': '',
        'token_shop': 105,
        'prize_money': 5,
        'auction': 2,
    },
    '8': {
        'info': '',
        'token_shop': 105,
        'prize_money': 10,
        'auction': 2,
    },
    '9': {
        'info': '',
        'token_shop': 105,
        'prize_money': 10,
        'auction': 3,
    },
    '10': {
        'info': '',
        'token_shop': 110,
        'prize_money': 10,
        'auction': 3,
    },
    '11': {
        'info': '',
        'token_shop': 110,
        'prize_money': 15,
        'auction': 3,
    },
    '12': {
        'info': '',
        'token_shop': 110,
        'prize_money': 15,
        'auction': 4,
    },
    '13': {
        'info': '',
        'token_shop': 115,
        'prize_money': 15,
        'auction': 4,
    },
    '14': {
        'info': '',
        'token_shop': 115,
        'prize_money': 20,
        'auction': 4,
    },
    '15': {
        'info': '',
        'token_shop': 115,
        'prize_money': 20,
        'auction': 5,
    },
    '16': {
        'info': '',
        'token_shop': 120,
        'prize_money': 20,
        'auction': 5,
    },
    '17': {
        'info': '',
        'token_shop': 120,
        'prize_money': 25,
        'auction': 5,
    },
    '18': {
        'info': '',
        'token_shop': 120,
        'prize_money': 25,
        'auction': 6,
    },
    '19': {
        'info': '',
        'token_shop': 125,
        'prize_money': 25,
        'auction': 6,
    },
    '20': {
        'info': '',
        'token_shop': 125,
        'prize_money': 30,
        'auction': 6,
    },


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

    level_data = ALL_LEVELS[str(level)]

    level_string = 'CURRENT SERVER LEVEL: **'+str(level)+'**'
    level_string += '\nCURRENT SERVER POINTS: **'+format(orig_points, ',')+'**'
    level_string += '\nPOINTS TO NEXT LEVEL: **'+format(points_to_next_level, ',')+'**'
    level_string += '\n-----------------------------------'
    level_string += '\nSERVER STATS:'
    level_string += '\nToken Shop Stock Added Per Week: **$'+str(level_data['token_shop'])+'**'
    level_string += '\nSOL Prize Money Added Per Week: **$'+str(level_data['prize_money'])+'**'
    level_string += '\nDaily Auction Prizes Tier: **Tier '+str(level_data['auction'])+'**'
    level_string += '\n-----------------------------------'
    level_string += '\nCurrent SOL Prize Pool'
    level_string += '\n-----------------------------------'

    await level_message.edit(content=level_string)

    if server_level != level:
        pass
    
    await message.channel.send('level: '+str(level)+' - points: '+str(num_points))

    

    

