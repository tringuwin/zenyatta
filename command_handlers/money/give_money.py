

from helpers import generic_find_user, valid_number_of_params
from safe_send import safe_send
from user.user import get_user_money


async def give_money(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, 'Invalid number of params')
        return
    
    user_id = params[1]
    num_money = float(params[2])

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find a matching user.')
        return
    
    user_money = get_user_money(user)
    new_money = user_money + num_money

    users = db['users']
    users.update_one({'discord_id': user['discord_id']}, {'$set': {'money': new_money}})

    await safe_send(message.channel, 'Money given')