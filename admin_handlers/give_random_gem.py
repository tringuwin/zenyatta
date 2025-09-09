
from common_messages import invalid_number_of_params
from helpers import generic_find_user, valid_number_of_params
from safe_send import safe_send
from user.user import get_user_gems
import constants
import random


async def give_random_gem_to_user(db, user):

    user_gems = get_user_gems(user)

    random_color = random.choice(constants.GEM_COLORS)
    user_gems[random_color] += 1

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}})

    return random_color


async def give_random_gem_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find that user.')
        return
    
    random_color = await give_random_gem_to_user(db, user)

    await safe_send(message.channel, 'User recieved 1 '+random_color+' gem.')