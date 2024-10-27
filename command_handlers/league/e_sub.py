
from helpers import generic_find_user, valid_number_of_params
from rewards import change_tokens, change_xp


async def e_sub_handler(client, db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await message.channel.send('Invalid number of params')
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('Could not find a matching user.')
        return
    
    await change_xp(db, user, 300, client)
    await change_tokens(db, user, 500, 'emergency-sub')
    await message.channel.send('Gave user 300 XP and 500 tokens for being an emergency sub.')