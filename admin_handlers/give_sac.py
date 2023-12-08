

from common_messages import invalid_number_of_params
from discord_actions import get_user_from_guild, give_role_to_user, member_has_role
from helpers import generic_find_user, valid_number_of_params

import time

import constants

async def give_sac_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_info = params[1]
    user = await generic_find_user(client, db, user_info)
    if not user:
        await message.channel.send('User not found. Maybe they have not registered yet?')
        return
    
    user_obj = await get_user_from_guild(client, user['discord_id'])
    if not user_obj:
        await message.channel.send('Error finding user.')
        return

    is_sac = member_has_role(user_obj, constants.SAC_ROLE)
    if is_sac:
        await message.channel.send('User already has the Supporter role.')
        return

    await give_role_to_user(client, user_obj, constants.SAC_ROLE)

    current_time = time.time()
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"last_sac": current_time}})

    await message.channel.send('User now has the Supporter role! It will last for 30 days before needing to be verified again.')


    

