

from command_handlers.bets.new_bet import get_team_payout_rate, total_tokens_on_team
from common_messages import not_registered_response
from discord_actions import get_guild
from user import get_user_bets, user_exists
import constants
import math

async def my_bets_handler(db, message, client):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    user_bets = get_user_bets(user)
    if len(user_bets) == 0:
        await message.channel.send('You do not have any current SOL match bets.')
        return
    
    final_string = '**YOUR SOL MATCH BETS:**'

    guild = await get_guild(client)

    bets = db['bets']
    index = 1
    for bet in user_bets:
        bet_string = '\n'+str(index)+'. '
        bet_obj = bets.find_one({'bet_id': bet['bet_id']})

        my_betters = 'team_1_betters'
        other_betters = 'team_2_betters'
        if bet_obj['team_2'] == bet['team']:
            my_betters = 'team_2_betters'
            other_betters = 'team_1_betters'

        my_total = total_tokens_on_team(bet_obj[my_betters])
        other_total = total_tokens_on_team(bet_obj[other_betters])

        payout_rate = get_team_payout_rate(my_total, other_total)
        payout = math.floor(payout_rate * float(bet['tokens']))

        team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[bet['team']]
        team_emoji = guild.get_emoji(team_emoji_id)
        bet_string += str(team_emoji)+' '+bet['team']+' | 🪙 '+str(bet['tokens'])+' | Potential Payout: '+str(payout)

        final_string += bet_string


    await message.channel.send(final_string)
    
