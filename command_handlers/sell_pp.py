

from common_messages import not_registered_response
from user import get_user_poke_points, user_exists


async def sell_pp_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response()
        return

    pp = get_user_poke_points(user)
    if pp < 10:
        await message.channel.send('Minimum amount of PokePoints that can be sold is 10.')
        return
    
    tokens_earned = 0
    sold_pp = 0
    while pp > 10:
        pp -= 10
        sold_pp += 10
        tokens_earned += 1

    users = db['users']
    users.update_one({'discord_id': message.author.id}, {'$set': {'tokens': user['tokens']+tokens_earned, 'poke_points': pp}})

    await message.channel.send('You sold '+str(sold_pp)+' for **'+str(tokens_earned)+' Tokens!**')

