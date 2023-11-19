
from common_messages import invalid_number_of_params
from helpers import generic_find_user, valid_number_of_params
from user import get_user_gems
import constants
import random


async def give_random_gem_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('Could not find that user.')
        return
    
    user_gems = get_user_gems(user)

    random_color = random.choice(constants.GEM_COLORS)
    user_gems[random_color] += 1

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}})

    await message.channel.send('User recieved 1 '+random_color+' gem.')