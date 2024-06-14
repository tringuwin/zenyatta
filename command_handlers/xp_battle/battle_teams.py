

from discord_actions import get_guild
from helpers import get_constant_value, set_constant_value
import random

from user import get_user_wlt, user_exists
import constants


async def battle_teams_handler(db, message, client):

    battle_info = get_constant_value(db, 'battle')

    if not battle_info['battle_on']:
        await message.channel.send('There is no battle right now.')
        return

    current_players = battle_info['current_players']

    current_players.append(constants.SPICY_RAGU_ID)

    players_with_wlt = []
    for player_id in current_players:
        if player_id == -1:
            players_with_wlt.append({'user_id': player_id, 'ratio': -1.0})
        else:
            user = user_exists(db, player_id)
            wlt = get_user_wlt(user)
            ratio = None
            if wlt['w'] == 0 and wlt['l'] == 0:
                ratio = 0.5
            else:
                ratio =  wlt['w'] / (wlt['w']+wlt['l'])
            players_with_wlt.append({'user_id': player_id, 'ratio': ratio})

    sorted_players = sorted(players_with_wlt, key=lambda x: x['ratio'], reverse=True)
        
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

    battle_info['current_teams'] = {
        'blue': blue_team,
        'red': red_team
    }

    set_constant_value(db, 'battle', battle_info)

    final_string = '**BLUE TEAM:**'
    user_index = 0
    for user_id in blue_team:
        if user_id == -1:
            final_string += '\n'+str(user_index)+'. '+'BOT 🤖'
        else:
            user = user_exists(db, user_id)
            final_string += '\n'+str(user_index)+'. '+user['battle_tag']

        user_index += 1

    final_string += '\n\n**RED TEAM:**'
    user_index = 0
    for user_id in red_team:
        if user_id == -1:
            final_string += '\n'+str(user_index)+'. '+'BOT 🤖'
        else:
            user = user_exists(db, user_id)
            final_string += '\n'+str(user_index)+'. '+user['battle_tag']

        user_index += 1
        
    await message.channel.send(final_string)

    guild = await get_guild(client)
    xp_battle_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)
    await xp_battle_channel.send(final_string)

