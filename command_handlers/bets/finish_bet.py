

from command_handlers.bets.new_bet import get_team_payout_rate, total_tokens_on_team
from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
import math

from rewards import change_tokens
from user.user import get_user_bets, user_exists
import constants

async def finish_bet(db, message, client, bet, team_won, team_loss):

    bet_id = bet['bet_id']

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
            print('Giving '+str(tokens_to_win)+' tokens to '+user['battle_tag'])
            await change_tokens(db, user, tokens_to_win, 'sol-bet')


    users = db['users']
    for winner_id in winning_betters:
        user = user_exists(db, int(winner_id))
        if user:
            user_bets = get_user_bets(user)
            if len(user_bets) == 0:
                continue

            final_user_bets = []
            for user_bet in user_bets:
                if user_bet['bet_id'] != bet_id:
                    final_user_bets.append(user_bet)

            users.update_one({"discord_id": user['discord_id']}, {"$set": {"bets": final_user_bets}})
    for loser_id in losing_betters:
        user = user_exists(db, int(loser_id))
        if user:
            user_bets = get_user_bets(user)
            if len(user_bets) == 0:
                continue

            final_user_bets = []
            for user_bet in user_bets:
                if user_bet['bet_id'] != bet_id:
                    final_user_bets.append(user_bet)

            users.update_one({"discord_id": user['discord_id']}, {"$set": {"bets": final_user_bets}})

    guild = await get_guild(client)
    bet_channel = guild.get_channel(constants.BET_CHANNEL_ID)

    bet_msg_title = await bet_channel.fetch_message(bet['bet_id'])
    bet_msg_1 = await bet_channel.fetch_message(bet['team_1_msg'])
    bet_msg_2 = await bet_channel.fetch_message(bet['team_2_msg'])
    await bet_msg_title.delete()
    await bet_msg_1.delete()
    await bet_msg_2.delete()

    bets = db['bets']
    bets.delete_one({'bet_id': bet_id})

    await message.channel.send('Bet payout complete')



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
    
    await finish_bet(db, message, client, bet, team_won, team_loss)
    