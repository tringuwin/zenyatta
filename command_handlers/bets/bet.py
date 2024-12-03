

import time
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from rewards import change_tokens
from user import get_league_team, get_user_bets, get_user_tokens, user_exists


def bet_is_expired(bet_obj):

    if 'timestamp' in bet_obj:
        current_time = time.time()
        if current_time > bet_obj['timestamp']:
            return True

    return False

def close_bet(bets, bet_obj):
    bets.update_one({'bet_id': bet_obj['bet_id']}, {'$set': {'open': False}})



async def bet_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    team_to_bet = params[1].lower()
    tokens_to_bet = params[2]

    if not can_be_int(tokens_to_bet):
        await message.channel.send(tokens_to_bet+' is not a number.')
        return
    tokens_to_bet = int(tokens_to_bet)

    if tokens_to_bet < 1:
        await message.channel.send('The minimum amount of tokens that can be bet is 1')
        return
    
    user_tokens = get_user_tokens(user)
    if tokens_to_bet > user_tokens:
        await message.channel.send('You do not have enough tokens for this bet.')
        return

    bets = db['bets']
    all_bets = bets.find()
    bet_team = None
    bet_obj = None
    other_team = None
    betters = None
    for bet in all_bets:

        if team_to_bet == bet['team_1'].lower():
            bet_team = bet['team_1']
            bet_obj = bet
            other_team = bet['team_2']
            betters = 'team_1_betters'
        if team_to_bet == bet['team_2'].lower():
            bet_team = bet['team_2']
            bet_obj = bet
            other_team = bet['team_1']
            betters = 'team_2_betters'

    if bet_team == None:
        await message.channel.send('There is no team named "'+params[1]+'" that can be bet on right now.')
        return
    
    if not bet_obj['open']:
        await message.channel.send('This match is not open for betting right now.')
        return
    
    if bet_is_expired(bet_obj):
        close_bet(bets, bet_obj)
        await message.channel.send('This match is not open for betting right now.')
        return
    
    player_league_team = get_league_team(user)
    if player_league_team == other_team:
        await message.channel.send('You cannot bet against the league team you are on.')
        return
    
    already_bet_on_match = False
    past_bet_on_team = None
    user_bets = get_user_bets(user)
    for bet in user_bets:
        if bet['bet_id'] == bet_obj['bet_id']:
            already_bet_on_match = True
            past_bet_on_team = bet['team']

    if already_bet_on_match and (past_bet_on_team != bet_team):
        await message.channel.send('You cannot bet on both teams in a match. You have already bet on '+past_bet_on_team+' for this match.')
        return
    
    await change_tokens(db, user, int(-1*tokens_to_bet), 'sol-bet')

    users = db['users']

    if already_bet_on_match:

        for bet in user_bets:
            if bet['bet_id'] == bet_obj['bet_id']:
                bet['tokens'] += tokens_to_bet
        
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"bets": user_bets}})
        
        bet_obj[betters][str(user['discord_id'])]['tokens'] += tokens_to_bet
        bets.update_one({'bet_id': bet_obj['bet_id']}, {"$set": {betters: bet_obj[betters]}})

    else:

        new_bet = {
            'bet_id': bet_obj['bet_id'],
            'team': bet_team,
            'tokens': tokens_to_bet
        }
        user_bets.append(new_bet)

        users.update_one({"discord_id": user['discord_id']}, {"$set": {"bets": user_bets}})

        bet_obj[betters][str(user['discord_id'])] = {
            'tokens': tokens_to_bet
        }

        bets.update_one({'bet_id': bet_obj['bet_id']}, {"$set": {betters: bet_obj[betters]}})        

    await message.channel.send('Bet placed successfully!')

    


        

