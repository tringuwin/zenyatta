

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
import constants


ALL_LEVELS = {


    '1': {
        'info': '$50 Token Shop Stock Added Per Week',
        'token_shop': 50,
        'prize_money': 0,
        'auction': 0,
    },
    '2': {
        'info': 'Tier 1 Daily Auctions',
        'token_shop': 50,
        'prize_money': 0,
        'auction': 1,
    },
    '3': {
        'info': '$75 Token Shop Stock Added Per Week',
        'token_shop': 75,
        'prize_money': 0,
        'auction': 1,
    },
    '4': {
        'info': '$100 Token Shop Stock Added Per Week',
        'token_shop': 100,
        'prize_money': 0,
        'auction': 1,
    },
    '5': {
        'info': '$5 SOL Prize Money Added Per Week',
        'token_shop': 100,
        'prize_money': 5,
        'auction': 1,
    },
    '6': {
        'info': 'Tier 2 Daily Auctions',
        'token_shop': 100,
        'prize_money': 5,
        'auction': 2,
    },
    '7': {
        'info': '$105 Token Shop Stock Added Per Week',
        'token_shop': 105,
        'prize_money': 5,
        'auction': 2,
    },
    '8': {
        'info': '$10 SOL Prize Money Added Per Week',
        'token_shop': 105,
        'prize_money': 10,
        'auction': 2,
    },
    '9': {
        'info': 'Tier 3 Daily Auctions',
        'token_shop': 105,
        'prize_money': 10,
        'auction': 3,
    },
    '10': {
        'info': '$110 Token Shop Stock Added Per Week',
        'token_shop': 110,
        'prize_money': 10,
        'auction': 3,
    },
    '11': {
        'info': '$15 SOL Prize Money Added Per Week',
        'token_shop': 110,
        'prize_money': 15,
        'auction': 3,
    },
    '12': {
        'info': 'Tier 4 Daily Auctions',
        'token_shop': 110,
        'prize_money': 15,
        'auction': 4,
    },
    '13': {
        'info': '$115 Token Shop Stock Added Per Week',
        'token_shop': 115,
        'prize_money': 15,
        'auction': 4,
    },
    '14': {
        'info': '$20 SOL Prize Money Added Per Week',
        'token_shop': 115,
        'prize_money': 20,
        'auction': 4,
    },
    '15': {
        'info': 'Tier 5 Daily Auctions',
        'token_shop': 115,
        'prize_money': 20,
        'auction': 5,
    },
    '16': {
        'info': '$120 Token Shop Stock Added Per Week',
        'token_shop': 120,
        'prize_money': 20,
        'auction': 5,
    },
    '17': {
        'info': '$25 SOL Prize Money Added Per Week',
        'token_shop': 120,
        'prize_money': 25,
        'auction': 5,
    },
    '18': {
        'info': 'Tier 6 Daily Auctions',
        'token_shop': 120,
        'prize_money': 25,
        'auction': 6,
    },
    '19': {
        'info': '$125 Token Shop Stock Added Per Week',
        'token_shop': 125,
        'prize_money': 25,
        'auction': 6,
    },
    '20': {
        'info': '$30 SOL Prize Money Added Per Week',
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
    level_string += '\nCurrent SOL Prize Pool: **$100**'
    level_string += '\n-----------------------------------'

    await level_message.edit(content=level_string)


    next_message = await server_level_channel.fetch_message(constants.NEXT_LEVELS_MESSAGE)
    
    next_string = '**NEXT 5 LEVELS**'
    level_copy = level
    for _ in range(5):
        level_copy += 1
        new_level_data = ALL_LEVELS[str(level_copy)]
        next_string += '\nLEVEL '+str(level_copy)+' ('+format((level_copy*5,000), ',')+' Points) : '+new_level_data['info']

    next_string += '\n-----------------------------------'

    await next_message.edit(content=next_string)


    if server_level != level:
        pass
    
    await message.channel.send('level: '+str(level)+' - points: '+str(num_points))

    

    

