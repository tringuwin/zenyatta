

from common_messages import invalid_number_of_params
from helpers import get_constant_value, set_constant_value, valid_number_of_params
from rewards import change_xp
from user import get_user_wlt, user_exists


XP_PER_WIN = 0
XP_PER_LOSS = 0
XP_PER_TIE = 0

async def battle_win_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_winner = params[1].lower()
    if team_winner != 'red' and team_winner != 'blue' and team_winner != 'tie':
        await message.channel.send('Invalid team name. Must be red, blue or tie.')
        return

    battle_info = get_constant_value(db, 'battle')

    if not battle_info['battle_on']:
        await message.channel.send('There is no battle right now.')
        return

    players_in_battle = []
    for team_name in battle_info['current_teams']:
        team = battle_info['current_teams'][team_name]
        for user_id in team:
            players_in_battle.append(user_id)

    battle_info['past_players'].append(players_in_battle)

    users = db['users']

    if team_winner == 'tie':

        for user_id in players_in_battle:
            user = user_exists(db, user_id)
            user_wlt = get_user_wlt(user)
            user_wlt['t'] += 1
            users.update_one({"discord_id": user['discord_id']}, {"$set": {"wlt": user_wlt}})
            await change_xp(db, user, XP_PER_TIE, client)

    else:
        
        win_team = battle_info['current_teams']['blue']
        lose_team = battle_info['current_teams']['red']
        if team_winner == 'red':
            win_team = battle_info['current_teams']['red']
            lose_team = battle_info['current_teams']['blue']

        for user_id in win_team:
            user = user_exists(db, user_id)
            user_wlt = get_user_wlt(user)
            user_wlt['w'] += 1
            users.update_one({"discord_id": user['discord_id']}, {"$set": {"wlt": user_wlt}})
            await change_xp(db, user, XP_PER_WIN, client)

        for user_id in lose_team:
            user = user_exists(db, user_id)
            user_wlt = get_user_wlt(user)
            user_wlt['l'] += 1
            users.update_one({"discord_id": user['discord_id']}, {"$set": {"wlt": user_wlt}})
            await change_xp(db, user, XP_PER_LOSS, client)


    battle_info['battle_on'] = False
    battle_info['reg_open'] = False

    set_constant_value(db, 'battle', battle_info)

    await message.channel.send('Winner recorded and battle ended.')
