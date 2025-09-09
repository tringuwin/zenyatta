

from command_handlers.xp_battle.battle_helpers import get_battle_constant_name, get_battle_upper_player_limit, get_battle_user_display
from discord_actions import get_guild
from helpers import can_be_int, get_constant_value, set_constant_value
import random
import constants

from safe_send import safe_edit, safe_send
from user.user import user_exists


async def update_players_message(client, final_string, battle_obj):

    guild = await get_guild(client)
    xp_battle_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)
    players_message = await xp_battle_channel.fetch_message(battle_obj['players_msg'])

    await safe_edit(players_message, content=final_string)

async def battle_no_show_handler(db, message, client, context):

    parts = message.content.split()
    if len(parts) != 2:
        await safe_send(message.channel, 'Need 2 params')
        return
    
    user_num = parts[1]

    if not can_be_int(user_num):
        await safe_send(message.channel, user_num+' is not a number')
        return
    
    user_num = int(user_num)
    upper_limit = get_battle_upper_player_limit(context)

    if user_num > upper_limit or user_num < 1:
        await safe_send(message.channel, 'Must be a number between 1 and '+str(upper_limit))
        return
    real_index = user_num - 1
    
    battle_constant_name = get_battle_constant_name(context)
    battle_obj = get_constant_value(db, battle_constant_name)

    if len(battle_obj['sign_ups']) == 0:

        battle_obj['current_players'][real_index] = -1
        set_constant_value(db, battle_constant_name, battle_obj)

        await safe_send(message.channel, 'No player, replacing with a bot.')
        final_string = '**PLAYERS IN XP BATTLE:**'

        index = 1
        for player_id in battle_obj['current_players']:

            if player_id == -1:
                final_string += '\n'+str(index)+'. '+'BOT 🤖'
            else:
                user = user_exists(db, player_id)
                user_display = get_battle_user_display(user, context)
                final_string += '\n'+str(index)+'. '+user_display+' | '+'<@'+str(user['discord_id'])+'>'

            index += 1

        await safe_send(message.channel, final_string)
        await update_players_message(client, final_string, battle_obj)
        return
    

    valid_players = battle_obj['player_pools']['valid_pool'] 

    found_player = None

    while not found_player:
        
        while len(valid_players) > 0 and (not found_player):
            index = random.randint(0, len(valid_players) - 1) 
            removed_item = valid_players.pop(index)
            battle_obj['sign_ups'].remove(removed_item)
            found_player = removed_item

        if not found_player:

            past_players = battle_obj['past_players']
            past_players.pop(0)
            battle_obj['past_players'] = past_players

    battle_obj['current_players'][real_index] = found_player

    set_constant_value(db, battle_constant_name, battle_obj)

    user = user_exists(db, found_player)
    user_display = get_battle_user_display(user, context)
    await safe_send(message.channel, 'Replacing with player '+user_display)

    final_string = '**PLAYERS IN XP BATTLE:**'
    index = 1
    for player_id in battle_obj['current_players']:

        user = user_exists(db, player_id)
        user_display = get_battle_user_display(user, context)
        final_string += '\n'+str(index)+'. '+user_display+' | '+'<@'+str(user['discord_id'])+'>'

        index += 1

    await safe_send(message.channel, final_string)

    await update_players_message(client, final_string, battle_obj)