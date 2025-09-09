
from common_messages import invalid_number_of_params
from helpers import generic_find_user, valid_number_of_params
from safe_send import safe_send


async def set_level_handler(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]
    level_to_set = int(params[2])

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find that user.')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"xp": 0, "level": level_to_set}})

    await safe_send(message.channel, 'Level set')