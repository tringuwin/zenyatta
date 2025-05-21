

from command_handlers.xp_battle.battle_helpers import create_battle_teams, get_battle_constant_name, get_battle_user_display, get_battle_user_wlt, get_blue_team_name, get_red_team_name
from discord_actions import get_guild
from helpers import get_constant_value, set_constant_value
import random

from user.user import user_exists
import constants


async def battle_teams_handler(db, message, client, context):

    battle_constant_name = get_battle_constant_name(context)
    battle_info = get_constant_value(db, battle_constant_name)

    if not battle_info['battle_on']:
        await message.channel.send('There is no battle right now.')
        return

    current_players = battle_info['current_players']

    current_players.append(constants.SPICY_RAGU_ID)

    players_with_wlt = []
    for player_id in current_players:
        if player_id == -1:
            players_with_wlt.append({'user_id': player_id, 'points': -1000.0})
        else:
            user = user_exists(db, player_id)
            wlt = get_battle_user_wlt(user, context)
            points = wlt['w'] - wlt['l']
            players_with_wlt.append({'user_id': player_id, 'points': points})

    sorted_players = sorted(players_with_wlt, key=lambda x: x['points'], reverse=True)
        
    team_1 = []
    team_2 = []

    team_val = 1
    for sorted_player in sorted_players:

        if team_val == 1:
            team_1.append(sorted_player['user_id'])
            team_val = 2
        else:
            team_2.append(sorted_player['user_id'])
            team_val = 1

    # put spicy first
    index = 0
    for team_player in team_1:
        if team_player == constants.SPICY_RAGU_ID:
            if index != 0:
                team_1[index] = team_1[0]
                team_1[0] = constants.SPICY_RAGU_ID
                break
        index += 1
    index = 0
    for team_player in team_2:
        if team_player == constants.SPICY_RAGU_ID:
            if index != 0:
                team_2[index] = team_2[0]
                team_2[0] = constants.SPICY_RAGU_ID
                break
        index += 1


    blue_team = []
    red_team = []

    team_1_color = random.choice(['blue', 'red'])
    if team_1_color == 'red':
        red_team = team_1
        blue_team = team_2
    else:
        red_team = team_2
        blue_team = team_1

    battle_info['current_teams'] = create_battle_teams(blue_team, red_team, context)

    set_constant_value(db, battle_constant_name, battle_info)

    blue_team_name = get_blue_team_name(context)
    red_team_name = get_red_team_name(context)

    final_string = f'**🔵 {blue_team_name} 🔵**'
    user_index = 0
    for user_id in blue_team:
        if user_id == -1:
            final_string += '\n'+str(user_index)+'. '+'BOT 🤖'
        else:
            user = user_exists(db, user_id)
            user_display = get_battle_user_display(user, context)
            final_string += '\n'+str(user_index)+'. '+user_display+' | '+'<@'+str(user['discord_id'])+'>'

        user_index += 1

    final_string += f'\n\n**🔴 {red_team_name} 🔴**'
    user_index = 0
    for user_id in red_team:
        if user_id == -1:
            final_string += '\n'+str(user_index)+'. '+'BOT 🤖'
        else:
            user = user_exists(db, user_id)
            user_display = get_battle_user_display(user, context)
            final_string += '\n'+str(user_index)+'. '+user_display+' | '+'<@'+str(user['discord_id'])+'>'

        user_index += 1
        
    await message.channel.send(final_string)

    guild = await get_guild(client)
    xp_battle_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)
    await xp_battle_channel.send(final_string)

