

from common_messages import invalid_number_of_params
from helpers import generic_find_user, get_constant_value, valid_number_of_params
from safe_send import safe_send
from user.user import get_user_vouchers


async def give_vouchers(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]
    num = int(params[2])

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find that user.')
        return

    free_vouchers = get_constant_value(db, 'free_vouchers')
    vouchers_to_give = min(num, free_vouchers)

    user_vouchers = get_user_vouchers(user)
    user_vouchers += vouchers_to_give

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"vouchers": user_vouchers}})

    await safe_send(message.channel, f'Vouchers given: {vouchers_to_give}')