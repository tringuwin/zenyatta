

from common_messages import invalid_number_of_params, not_registered_response
from helpers import get_constant_value, set_constant_value, valid_number_of_params
from user import get_user_packs, user_exists


async def redeem_code(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    code = params[1].upper()

    pack_codes = get_constant_value(db, 'pack_codes')
    if code not in pack_codes:
        await message.channel.send('Invalid code.')
        return
    
    pack_codes.remove(code)
    set_constant_value(db, 'pack_codes', pack_codes)

    user_packs = get_user_packs(user)
    new_packs = user_packs + 1
    users = db['users']
    users.update_one({'discord_id': message.author.id}, {'$set': {'packs': new_packs}})

    await message.channel.send('Code redeemed! You were given an SOL Card Pack.')
