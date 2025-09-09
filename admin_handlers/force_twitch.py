

from common_messages import invalid_number_of_params
from helpers import generic_find_user, valid_number_of_params
from safe_send import safe_send


async def force_twitch_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    user_id = params[1]

    pi_pi_chan = await generic_find_user(client, db, user_id)
    if not pi_pi_chan:
        await safe_send(message.channel, 'User not found.')
        return
    
    twitch_name = params[2]
    
    users = db['users']
    users.update_one({"discord_id": pi_pi_chan['discord_id']}, {"$set": {"twitch": twitch_name, "twitch_lower": twitch_name.lower()}})

    await safe_send(message.channel, 'Twitch set for user.')
