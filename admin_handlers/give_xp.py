

from helpers import can_be_int, generic_find_user, valid_number_of_params
from rewards import change_xp
from safe_send import safe_send


async def give_xp_handler(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, 'Invalid number of params')
        return
    
    if not can_be_int(params[2]):
        await safe_send(message.channel, '"'+params[2]+'" is not a number.')
        return

    user_id = params[1]
    num_xp = int(params[2])

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find a matching user.')
        return
    
    await change_xp(db, user, num_xp, client)
    await safe_send(message.channel, 'XP given')