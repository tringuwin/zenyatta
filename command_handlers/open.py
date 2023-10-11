
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
from rewards import change_pickaxes, change_tokens
from user import get_user_gems, get_user_lootboxes, user_exists
import random
import constants



lootboxes = {

    '2': [
        ['Pickaxe', 1, 50],
        ['Gem', 1, 95],
        ['Token', 200, 100]
    ],

    '3': [

    ]


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
    if not can_be_int(box_num):
        await message.channel.send(box_num+' is not a valid lootbox number.')
        return
    
    box_num = int(box_num)
    user_boxes = get_user_lootboxes(user)
    if not (box_num in user_boxes):
        await message.channel.send('You do not have that lootbox!')
        return
    
    user_boxes.remove(box_num)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"lootboxes": user_boxes}})

    random_int = random.randint(1, 100)
    
    lootbox_info = lootboxes[str(box_num)]

    prize = None
    for possible_prize in lootbox_info:
        if random_int <= possible_prize[2]:
            prize = possible_prize
            break

    final_string = 'You opened your Level '+str(box_num)+' Lootbox and found... '
    if prize[0] == 'Token':
        final_string += str(prize[1])+" Tokens!! 🪙"
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

        final_string += str(gem_emoji)

        user_gems = get_user_gems(user)
        user_gems[gem_color] += prize[1]
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}}) 
    elif prize[0] == 'Pickaxe':
        
        if prize[1] == 1:
            final_string += '1 Pickaxe!! ⛏️'
        else:
            final_string += str(prize[1])+' Pickaxes!! ⛏️'

        await change_pickaxes(db, user, prize[1])

    await message.channel.send(final_string)



    

    

    
