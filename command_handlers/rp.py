


from helpers import can_be_int, generic_find_user, valid_number_of_params
from rewards import change_packs, change_tokens
from safe_send import safe_send


async def rp_handler(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, 'Invalid number of params')
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find a matching user.')
        return
    
    points = params[2]
    if not can_be_int(points):
        await safe_send(message.channel, points+' is not a number')
        return
    
    points = int(points)

    pack_points = round(float(float(points) / 100.0), 2)
    
    await change_tokens(db, user, points, 'rogue-points')
    await change_packs(db, user, pack_points)
    await safe_send(message.channel, f'Gave user {points} tokens and {pack_points} packs for their Rogue Order')