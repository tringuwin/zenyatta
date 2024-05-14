
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
from rewards import change_pickaxes, change_tokens
from user import get_sub_lootboxes, get_user_gems, get_user_lootboxes, user_exists
import random
import constants



lootboxes = {

    'twitch': [
        ['Gem', 1, 20],
        ['Gem', 2, 35],
        ['Gem', 3, 45],
        ['Gem', 4, 50],
        ['Gem', 5, 55],
        ['Token', 100, 75],
        ['Token', 200, 85],
        ['Token', 300, 90],
        ['Token', 400, 95],
        ['Token', 500, 100]
    ],

    '2': [
        ['Pickaxe', 1, 50],
        ['Gem', 1, 95],
        ['Token', 200, 100]
    ],

    '3': [
        ['Pickaxe', 3, 50],
        ['Gem', 1, 80],
        ['Gem', 2, 95],
        ['Token', 200, 100]
    ],

    '4': [
        ['Pickaxe', 3, 40],
        ['Pickaxe', 5, 65],
        ['Gem', 1, 80],
        ['Gem', 2, 95],
        ['Token', 200, 100]
    ],

    '5': [
        ['Pickaxe', 5, 50],
        ['Pickaxe', 10, 77],
        ['Gem', 2, 92],
        ['Gem', 3, 97],
        ['Token', 300, 100]
    ],

    '6': [
        ['Pickaxe', 5, 35],
        ['Pickaxe', 10, 65],
        ['Gem', 2, 85],
        ['Gem', 3, 95],
        ['Token', 300, 100]
    ],

    '7': [
        ['Pickaxe', 10, 50],
        ['Pickaxe', 15, 70],
        ['Gem', 2, 90],
        ['Gem', 3, 95],
        ['Token', 300, 100]
    ],

    '8': [
        ['Pickaxe', 10, 35],
        ['Pickaxe', 15, 65],
        ['Gem', 3, 85],
        ['Gem', 4, 95],
        ['Token', 400, 100]
    ],

    '9': [
        ['Pickaxe', 15, 30],
        ['Pickaxe', 20, 50],
        ['Gem', 3, 65],
        ['Gem', 4, 80],
        ['Token', 200, 95],
        ['Token', 400, 100]
    ],

    '10': [
        ['Pickaxe', 15, 25],
        ['Pickaxe', 20, 50],
        ['Gem', 3, 65],
        ['Gem', 4, 80],
        ['Token', 300, 90],
        ['Token', 400, 100]
    ],

    '11': [
        ['Pickaxe', 15, 20],
        ['Pickaxe', 20, 40],
        ['Gem', 3, 60],
        ['Gem', 4, 80],
        ['Token', 400, 100],
    ],

    '12': [
        ['Pickaxe', 20, 30],
        ['Gem', 3, 60],
        ['Gem', 4, 80],
        ['Token', 400, 100],
    ],

    '13': [
        ['Pickaxe', 20, 15],
        ['Pickaxe', 25, 30],
        ['Gem', 3, 60],
        ['Gem', 4, 80],
        ['Token', 400, 100],
    ],

    '14': [
        ['Pickaxe', 20, 20],
        ['Pickaxe', 25, 35],
        ['Gem', 3, 55],
        ['Gem', 4, 80],
        ['Token', 400, 100],
    ],

    '15': [
        ['Pickaxe', 20, 35],
        ['Gem', 4, 70],
        ['Token', 400, 100],
    ],

    '16': [
        ['Pickaxe', 20, 30],
        ['Gem', 4, 60],
        ['Token', 400, 90],
        ['Token', 500, 100],
    ],

    '17': [
        ['Pickaxe', 20, 30],
        ['Gem', 4, 60],
        ['Token', 400, 80],
        ['Gem', 5, 90],
        ['Token', 500, 100],
    ],

    '18': [
        ['Pickaxe', 20, 30],
        ['Gem', 4, 50],
        ['Token', 400, 70],
        ['Gem', 5, 90],
        ['Token', 500, 100],
    ],

    '19': [
        ['Pickaxe', 20, 20],
        ['Gem', 4, 40],
        ['Token', 400, 60],
        ['Gem', 5, 80],
        ['Token', 500, 100],
    ],

    '20': [
        ['Gem', 4, 25],
        ['Token', 400, 50],
        ['Gem', 5, 75],
        ['Token', 500, 100],
    ],

}


async def open_handler(db, message, client):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    box_num = params[1]
    dict_key = ''
    is_sub_box = False

    users = db['users']

    if box_num.lower() == 'twitch':
        is_sub_box = True

        sub_lootboxes = get_sub_lootboxes(user)
        if sub_lootboxes < 1:
            await message.channel.send('You do not have any twitch lootboxes right now.')
            return
        
        sub_lootboxes -= 1
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"sub_lootboxes": sub_lootboxes}})

        dict_key = 'twitch'

    else:

        if not can_be_int(box_num):
            await message.channel.send(box_num+' is not a valid lootbox number.')
            return
        
        box_num = int(box_num)
        user_boxes = get_user_lootboxes(user)
        if not (box_num in user_boxes):
            await message.channel.send('You do not have that lootbox!')
            return
        
        user_boxes.remove(box_num)
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"lootboxes": user_boxes}})

        if box_num > 20:
            box_num = 20
        dict_key = str(box_num)
    
    random_int = random.randint(1, 100)
    lootbox_info = lootboxes[dict_key]

    prize = None
    for possible_prize in lootbox_info:
        if random_int <= possible_prize[2]:
            prize = possible_prize
            break

    final_string = 'You openened your Twitch Lootbox and found... **'
    if not is_sub_box:
        final_string = 'You opened your Level '+str(box_num)+' Lootbox and found... **'

    if prize[0] == 'Token':
        final_string += str(prize[1])+" Tokens!!** 🪙"
        await change_tokens(db, user, prize[1])
    elif prize[0] == 'Gem':

        guild = await get_guild(client)

        gem_color = random.choice(constants.GEM_COLORS)
        gem_emoji_id = constants.COLOR_TO_EMOJI_ID[gem_color]
        gem_emoji = guild.get_emoji(gem_emoji_id)

        if prize[1] == 1:
            final_string += '1 Gem!! '
        else:
            final_string += str(prize[1])+' Gems!! '

        final_string += "**"+str(gem_emoji)

        user_gems = get_user_gems(user)
        user_gems[gem_color] += prize[1]
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}}) 
    elif prize[0] == 'Pickaxe':
        
        if prize[1] == 1:
            final_string += '1 Pickaxe!!** ⛏️'
        else:
            final_string += str(prize[1])+' Pickaxes!!** ⛏️'

        await change_pickaxes(db, user, prize[1])

    await message.channel.send(final_string)



    

    

    
