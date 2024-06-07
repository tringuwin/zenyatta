

from common_messages import not_registered_response
from user import get_user_bets, user_exists


async def my_bets_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    user_bets = get_user_bets(user)
    if len(user_bets) == 0:
        await message.channel.send('You do not have any current SOL match bets.')
        return
    
    final_string = '**YOUR SOL MATCH BETS:**'

    bets = db['bets']
    index = 1
    for bet in user_bets:
        bet_string = '\n'+str(index)+'. '
        bet_obj = bets.find_one({'bet_id': bet['bet_id']})
        bet_string += bet['team']+' | 🪙 '+str(bet['tokens'])



    await message.channel.send(final_string)
    
