

from command_handlers.bets.new_bet import get_team_payout_rate, total_tokens_on_team
from helpers import can_be_int, valid_number_of_params
import math

from user import user_exists

async def finish_bet_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)

    if not valid_params:
        await message.channel.send('need 3 params')
        return
    
    bet_id = params[1]

    if not can_be_int(bet_id):
        await message.channel.send(bet_id+' is not a number')
        return
    bet_id  = int(bet_id)

    bets = db['bets']
    bet = bets.find_one({'bet_id': bet_id})
    if not bet:
        await message.channel.send('Bet with id not found.')
        return    

    team_won_input = params[2].lower()
    team_won = None
    team_loss = None
    if team_won_input == bet['team_1'].lower():
        team_won = '1'
        team_loss = '2'
    if team_won_input == bet['team_2'].lower():
        team_won = '2'
        team_loss = '1'

    if not team_won:
        await message.channel.send('That is not a valid team name for this match.')
        return
    
    winning_betters = bet['team_'+team_won+'_betters']
    losing_betters = bet['team_'+team_loss+'_betters']

    total_winner_pot = total_tokens_on_team(winning_betters)
    total_loser_pot = total_tokens_on_team(losing_betters)

    winner_payout_rate = get_team_payout_rate(total_winner_pot, total_loser_pot)

    for winner_id in winning_betters:

        winner = winning_betters[winner_id]
        tokens_bet = winner['tokens']
        tokens_to_win = math.floor(winner_payout_rate * float(tokens_bet))

        user = user_exists(db, int(winner_id))
        if user:

            await message.channel.send('Giving '+str(tokens_to_win)+' tokens to '+user['battle_tag'])

    await message.channel.send('Bet payout complete')

