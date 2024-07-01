


from helpers import can_be_int, generic_find_user, valid_number_of_params
from rewards import change_packs, change_tokens


async def rp_handler(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await message.channel.send('Invalid number of params')
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('Could not find a matching user.')
        return
    
    points = params[2]
    if not can_be_int(points):
        await message.channel.send(points+' is not a number')
        return
    
    points = int(points)

    pack_points = round(float(float(points) / 100.0), 2)
    
    await change_tokens(db, user, points)
    await change_packs(db, user, pack_points)
    await message.channel.send(f'Gave user {points} tokens and {pack_points} packs for their Rogue Order')