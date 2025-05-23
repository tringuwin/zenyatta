

from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
from user.user import get_user_bets, user_exists
import constants

async def void_bet_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)

    if not valid_params:
        await message.channel.send('need 2 params')
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
    
    betters_1 = bet['team_1_betters']
    betters_2 = bet['team_2_betters']


    users = db['users']
    for better_id in betters_1:
        user = user_exists(db, int(better_id))
        if user:
            user_bets = get_user_bets(user)
            if len(user_bets) == 0:
                continue

            final_user_bets = []
            for user_bet in user_bets:
                if user_bet['bet_id'] != bet_id:
                    final_user_bets.append(user_bet)

            bet_tokens = betters_1[better_id]['tokens']
            users.update_one({"discord_id": user['discord_id']}, {"$set": {"bets": final_user_bets, "tokens": user['tokens'] + bet_tokens}})
    for better_id in betters_2:
        user = user_exists(db, int(better_id))
        if user:
            user_bets = get_user_bets(user)
            if len(user_bets) == 0:
                continue

            final_user_bets = []
            for user_bet in user_bets:
                if user_bet['bet_id'] != bet_id:
                    final_user_bets.append(user_bet)

            bet_tokens = betters_2[better_id]['tokens']
            users.update_one({"discord_id": user['discord_id']}, {"$set": {"bets": final_user_bets, "tokens": user['tokens'] + bet_tokens}})
   

    guild = await get_guild(client)
    bet_channel = guild.get_channel(constants.BET_CHANNEL_ID)

    bet_msg_title = await bet_channel.fetch_message(bet['bet_id'])
    bet_msg_1 = await bet_channel.fetch_message(bet['team_1_msg'])
    bet_msg_2 = await bet_channel.fetch_message(bet['team_2_msg'])
    await bet_msg_title.delete()
    await bet_msg_1.delete()
    await bet_msg_2.delete()

    bets.delete_one({'bet_id': bet_id})

    await message.channel.send('Bet void complete')