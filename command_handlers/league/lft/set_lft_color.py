
from command_handlers.lft import get_lft_user
from common_messages import invalid_number_of_params, not_registered_response
from helpers import is_valid_hex_code, valid_number_of_params
from user import user_exists





async def set_lft_color_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    hex_code = params[1]
    if not is_valid_hex_code(hex_code):
        await message.channel.send(hex_code+' is not a valid hex code.')
        return

    created, lft_user = get_lft_user(db, message.author, user)

    lft_users = db['lft_users']
    if created:
        lft_user['profile_color'] = hex_code
        lft_users.insert_one(lft_user)
    else:
        lft_users.update_one({"user_id": lft_user['user_id']}, {"$set": {"profile_color": hex_code}})

    await message.channel.send('LFT Profile color set.')