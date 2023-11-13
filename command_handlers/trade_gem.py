
from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from user import get_gem_offer, get_user_gems, user_exists
import constants
import time

async def trade_gem_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    if len(message.mentions) != 1:
        await message.channel.send('Please mention 1 user to trade gems with.')
        return
    
    mentioned_member = message.mentions[0]
    other_user = user_exists(db, mentioned_member.id)
    if not other_user:
        await message.channel.send('The user you mentioned is not registered yet.')
        return
    
    color_to_give = params[1].lower()
    if not color_to_give in constants.DEFAULT_GEMS:
        await message.channel.send(color_to_give+' is not a valid gem color')
        return
    
    color_to_get = params[3].lower()
    if not color_to_get in constants.DEFAULT_GEMS:
        await message.channel.send(color_to_get+' is not a valid gem color')
        return
    
    user_gems = get_user_gems(user)
    count_of_color = user_gems[color_to_give]
    if count_of_color < 1:
        await message.channel.send('You do not have any '+color_to_give+' gems.')
        return
    
    other_user_gems = get_user_gems(other_user)
    other_count_of_color = other_user_gems[color_to_get]
    if other_count_of_color < 1:
        await message.channel.send('That user does not have any '+color_to_get+' gems.')
        return
    
    other_user_offer = get_gem_offer(other_user)
    if other_user_offer:
        await message.channel.send('That user already has a pending gem trade offer.')
        return
    
    new_offer = {
        'time_sent': time.time(),
        'sender_id': user['discord_id'],
        'sender_offer': color_to_give,
        'sender_wants': color_to_get
    }

    users = db['users']
    users.update_one({"discord_id": other_user['discord_id']}, {"$set": {"gem_offer": new_offer}})

    await message.channel.send('Gem trade offer sent! It will expire in 5 minutes.')