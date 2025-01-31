

from command_handlers.xp_battle.battle_helpers import get_battle_constant_name, get_battle_team_names, get_battle_user_wlt, get_wlt_constant_name
from common_messages import invalid_number_of_params
from discord_actions import get_guild
from helpers import get_constant_value, set_constant_value, valid_number_of_params
from rewards import change_xp
from user import get_user_wlt, user_exists
import constants


XP_PER_WIN = 300
XP_PER_LOSS = 50
XP_PER_TIE = 100

async def battle_win_handler(db, message, client, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_winner = params[1].lower()
    battle_team_names = get_battle_team_names(context)
    red_team = battle_team_names[0]
    blue_team = battle_team_names[1]
    if team_winner != red_team and team_winner != blue_team and team_winner != 'tie':
        await message.channel.send(f'Invalid team name. Must be {red_team}, {blue_team} or tie.')
        return

    battle_constant_name = get_battle_constant_name(context)
    battle_info = get_constant_value(db, battle_constant_name)

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
            if user_id == -1:
                continue
            user = user_exists(db, user_id)
            user_wlt = get_battle_user_wlt(user)
            user_wlt['t'] += 1
            wlt_constant_name = get_wlt_constant_name(context)
            users.update_one({"discord_id": user['discord_id']}, {"$set": {wlt_constant_name: user_wlt}})
            await change_xp(db, user, XP_PER_TIE, client)

    else:
        
        win_team = battle_info['current_teams'][blue_team]
        lose_team = battle_info['current_teams'][red_team]
        if team_winner == red_team:
            win_team = battle_info['current_teams'][red_team]
            lose_team = battle_info['current_teams'][blue_team]

        #
        for user_id in win_team:
            if user_id == -1:
                continue
            user = user_exists(db, user_id)
            user_wlt = get_battle_user_wlt(user, context)
            user_wlt['w'] += 1
            wlt_constant_name = get_wlt_constant_name(context)
            users.update_one({"discord_id": user['discord_id']}, {"$set": {wlt_constant_name: user_wlt}})
            await change_xp(db, user, XP_PER_WIN, client)

        for user_id in lose_team:
            if user_id == -1:
                continue
            user = user_exists(db, user_id)
            user_wlt = get_battle_user_wlt(user, context)
            user_wlt['l'] += 1
            wlt_constant_name = get_wlt_constant_name(context)
            users.update_one({"discord_id": user['discord_id']}, {"$set": {wlt_constant_name: user_wlt}})
            await change_xp(db, user, XP_PER_LOSS, client)


    battle_info['battle_on'] = False
    battle_info['reg_open'] = False

    set_constant_value(db, battle_constant_name, battle_info)

    await message.channel.send('Winner recorded and battle ended.')

    blue_team_upper = blue_team.upper()
    red_team_upper = red_team.upper()
    final_string = None
    if team_winner == 'tie':
        final_string = f'**⚪ BATTLE IS A DRAW! ⚪**\Team {blue_team_upper} gets **'+str(XP_PER_TIE)+f' XP each**\nTeam {red_team_upper} gets **'+str(XP_PER_TIE)+' XP each**'
    elif team_winner == 'overwatch':
        final_string = f'**🔵 {blue_team_upper} WINS! 🔵**\nTeam {blue_team_upper} gets **'+str(XP_PER_WIN)+f' XP each**\nTeam {red_team_upper} gets **'+str(XP_PER_LOSS)+' XP each**'
    else:
        final_string = f'**🔴 {red_team_upper} WINS! 🔴**\nTeam {red_team_upper} gets **'+str(XP_PER_WIN)+f' XP each**\nTeam {blue_team_upper} gets **'+str(XP_PER_LOSS)+' XP each**'

    guild = await get_guild(client)
    xp_battle_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)
    await xp_battle_channel.send(final_string)
