

from common_messages import invalid_number_of_params
from discord_actions import get_guild
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
        'info': '$5 Average Daily Auctions',
        'token_shop': 50,
        'prize_money': 0,
        'auction': 5,
    },
    '3': {
        'info': '$75 Token Shop Stock Added Per Week',
        'token_shop': 75,
        'prize_money': 0,
        'auction': 5,
    },
    '4': {
        'info': '$100 Token Shop Stock Added Per Week',
        'token_shop': 100,
        'prize_money': 0,
        'auction': 5,
    },
    '5': {
        'info': '$5 SOL Prize Money Added Per Week',
        'token_shop': 100,
        'prize_money': 5,
        'auction': 5,
    },
    '6': {
        'info': '$6 Average Daily Auctions',
        'token_shop': 100,
        'prize_money': 5,
        'auction': 6,
    },
    '7': {
        'info': '$105 Token Shop Stock Added Per Week',
        'token_shop': 105,
        'prize_money': 5,
        'auction': 6,
    },
    '8': {
        'info': '$10 SOL Prize Money Added Per Week',
        'token_shop': 105,
        'prize_money': 10,
        'auction': 6,
    },
    '9': {
        'info': '$7 Average Daily Auctions',
        'token_shop': 105,
        'prize_money': 10,
        'auction': 7,
    },
    '10': {
        'info': '$110 Token Shop Stock Added Per Week',
        'token_shop': 110,
        'prize_money': 10,
        'auction': 7,
    },
    '11': {
        'info': '$15 SOL Prize Money Added Per Week',
        'token_shop': 110,
        'prize_money': 15,
        'auction': 7,
    },
    '12': {
        'info': '$8 Average Daily Auctions',
        'token_shop': 110,
        'prize_money': 15,
        'auction': 8,
    },
    '13': {
        'info': '$115 Token Shop Stock Added Per Week',
        'token_shop': 115,
        'prize_money': 15,
        'auction': 8,
    },
    '14': {
        'info': '$20 SOL Prize Money Added Per Week',
        'token_shop': 115,
        'prize_money': 20,
        'auction': 8,
    },
    '15': {
        'info': '$9 Average Daily Auctions',
        'token_shop': 115,
        'prize_money': 20,
        'auction': 9,
    },
    '16': {
        'info': '$120 Token Shop Stock Added Per Week',
        'token_shop': 120,
        'prize_money': 20,
        'auction': 9,
    },
    '17': {
        'info': '$25 SOL Prize Money Added Per Week',
        'token_shop': 120,
        'prize_money': 25,
        'auction': 9,
    },
    '18': {
        'info': '$10 Average Daily Auctions',
        'token_shop': 120,
        'prize_money': 25,
        'auction': 10,
    },
    '19': {
        'info': '$125 Token Shop Stock Added Per Week',
        'token_shop': 125,
        'prize_money': 25,
        'auction': 10,
    },
    '20': {
        'info': '$30 SOL Prize Money Added Per Week',
        'token_shop': 125,
        'prize_money': 30,
        'auction': 10,
    },


}


def level_to_prize_money(level):

    return ALL_LEVELS[str(level)]['prize_money']

def level_to_token_shop_cash(level):
    
    return ALL_LEVELS[str(level)]['token_shop']

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
    prize_money_obj = constants_db.find_one({'name': 'prize_money'})
    prize_money = prize_money_obj['value']

    points_to_next_level = 5000 - num_points

    server_level_channel = client.get_channel(constants.SERVER_LEVEL_CHANNEL)
    level_message = await server_level_channel.fetch_message(constants.SERVER_LEVEL_MESSAGE)

    past_level_data = ALL_LEVELS[str(server_level)]
    level_data = ALL_LEVELS[str(level)]

    level_string = 'CURRENT SERVER LEVEL: **'+str(level)+'**'
    level_string += '\nCURRENT SERVER POINTS: **'+format(orig_points, ',')+'**'
    level_string += '\nPOINTS TO NEXT LEVEL: **'+format(points_to_next_level, ',')+'**'
    level_string += '\n-----------------------------------'
    level_string += '\nSERVER STATS:'
    level_string += '\nToken Shop Stock Added Per Week: **$'+str(level_data['token_shop'])+'**'
    level_string += '\nSOL Prize Money Added Per Week: **$'+str(level_data['prize_money'])+'**'
    level_string += '\nAverage Daily Auction Value: **$'+str(level_data['auction'])+'**'
    level_string += '\n-----------------------------------'
    level_string += '\nCurrent SOL Prize Pool: **$'+str(int(prize_money))+'**'
    level_string += '\n-----------------------------------'

    await level_message.edit(content=level_string)


    next_message = await server_level_channel.fetch_message(constants.NEXT_LEVELS_MESSAGE)
    
    next_string = '**NEXT 5 LEVELS**'
    level_copy = level
    for _ in range(5):
        level_copy += 1
        new_level_data = ALL_LEVELS[str(level_copy)]
        points_for_level = int(level_copy * 5000)
        next_string += '\nLEVEL '+str(level_copy)+' ('+format(points_for_level, ',')+' Points) : '+new_level_data['info']

    next_string += '\n-----------------------------------'

    await next_message.edit(content=next_string)


    if server_level != level:
        
        # make updates
        constants_db.update_one({"name": 'server_level'}, {"$set": {"value": {"level": level}}})

        guild = await get_guild(client)
        announcements_channel = guild.get_channel(constants.ANNOUNCEMENTS_CHANNEL_ID)

        changed_word = 'decreased'
        if level > server_level:
            changed_word = 'increased'

        changed_string = 'What Changed:'

        if past_level_data['token_shop'] != level_data['token_shop']:
            changed_string += '\n- Weekly Token Shop stock has ' +changed_word+ ' from **$'+str(past_level_data['token_shop'])+'** to **$'+str(level_data['token_shop'])+'**'

        if past_level_data['prize_money'] != level_data['prize_money']:
            changed_string += '\n- Weekly SOL Prize money has ' +changed_word+ ' from **$'+str(past_level_data['prize_money'])+'** to **$'+str(level_data['prize_money'])+'**'

        if past_level_data['auction'] != level_data['auction']:
            changed_string += '\n- Average Daily Auction value has ' +changed_word+ ' from **$'+str(past_level_data['auction'])+'** to **$'+str(level_data['auction'])+'**'

        final_string = '🌟 **SERVER LEVEL UPDATE** 🌟\n\n'

        if level > server_level:
            final_string += 'The server level has ***INCREASED*** from **LEVEL '+str(server_level)+'** to **LEVEL '+str(level)+'**'
            final_string += '\n\n'+changed_string
            final_string += '\n\nThank you to everyone who contributed! You can see the full list of rewards and how to contribute here: https://discord.com/channels/1130553449491210442/1234932215482155048' 
        else:
            final_string += 'The server level has *decreased* from **LEVEL '+str(server_level)+'** to **LEVEL '+str(level)+'**'
            final_string += '\n\n'+changed_string
            final_string += '\n\nThe server level impacts things like Token Shop Stock, Daily Auctions, and SOL Prize money. Find out how you can contribute here: https://discord.com/channels/1130553449491210442/1234932215482155048' 

        await announcements_channel.send(final_string)
    
    await message.channel.send('level: '+str(level)+' - points: '+str(num_points))

    

    

