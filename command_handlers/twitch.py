

from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from safe_send import safe_send
from user.user import twitch_user_exists, user_exists


async def twitch_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    twitch_username = params[1]
    if len(twitch_username) > 30:
        await safe_send(message.channel, twitch_username+' is too long to be a Twitch username.')
        return
    
    # ensure @ character is not included anywhere in the string
    if '@' in twitch_username:
        await safe_send(message.channel, 'Twitch username cannot contain the "@" character.')
        return

    twitch_linked = twitch_user_exists(db, twitch_username)
    if twitch_linked:
        await safe_send(message.channel, 'The twitch username "'+twitch_username+'" has already been linked to an account. Maybe you already linked it? If you think this is a mistake, contact staff by making a support ticket.')
        return
    
    twitch_lower = twitch_username.lower()

    users = db['users']
    users.update_one({'discord_id': user['discord_id']}, {"$set": {"twitch_lower": twitch_lower, "twitch": twitch_username}})

    await safe_send(message.channel, 'Success! You linked your Twitch to Spicy Esports. If you change your twitch username, please use this command again. *(Please note, this command will not give you the Twitch Subscriber role in this Discord. That must be done in by linking your Twitch in the Discord connections settings)*')
