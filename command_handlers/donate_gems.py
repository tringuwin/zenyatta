

from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from user import get_user_gems, user_exists
import constants

async def donate_gems(db, message):

    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    mentioned_users = message.mentions
    if len(mentioned_users) != 1:
        await message.channel.send('You must mention exactly one user to donate gems to.')
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_to_donate = user_exists(db, mentioned_users[0].id)
    if not user_to_donate:
        await message.channel.send('The user you mentioned is not registered.')
        return
    
    gem_color = params[2]
    gem_color_lower = gem_color.lower()
    if not gem_color_lower in constants.GEM_COLORS:
        await message.channel.send(gem_color+' is not a valid gem color.')
        return
    
    amount = params[3]
    if (not can_be_int(amount)):
        await message.channel.send(amount+' is not a valid number.')
        return
    
    amount = int(amount)
    if amount < 1:
        await message.channel.send('You must donate at least 1 gem.')
        return
    
    user_gems = get_user_gems(user)
    if user_gems[gem_color_lower] < amount:
        await message.channel.send('You do not have '+str(amount)+' '+gem_color+' gems to donate.')
        return
    
    user_gems[gem_color_lower] -= amount
    donate_user_gems = get_user_gems(user_to_donate)
    donate_user_gems[gem_color_lower] += amount

    users = db['users']
    users.update_one({'discord_id': user['discord_id']}, {'$set': {'gems': user_gems}})
    users.update_one({'discord_id': user_to_donate['discord_id']}, {'$set': {'gems': donate_user_gems}})

    await message.channel.send('You have donated '+str(amount)+' '+gem_color+' gems!')

    

    

