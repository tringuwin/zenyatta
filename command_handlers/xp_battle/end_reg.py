

from command_handlers.xp_battle.battle_helpers import get_battle_constant_name, get_battle_upper_player_limit, get_battle_user_display
from discord_actions import get_guild
from helpers import get_constant_value, set_constant_value
from safe_send import safe_send
from user.user import user_exists
from xp_battles import init_player_pools
import random
import constants

async def end_reg_handler(db, message, client, context):

    battle_constant_name = get_battle_constant_name(context)
    battle_info = get_constant_value(db, battle_constant_name)

    if not battle_info['battle_on']:
        await safe_send(message.channel, 'There is no battle right now.')
        return

    if not battle_info['reg_open']:
        await safe_send(message.channel, 'Registration is not open for this battle right now.')
        return

    number_sign_ups = len(battle_info['sign_ups'])
    battle_upper_limit = get_battle_upper_player_limit(context)
    if number_sign_ups < battle_upper_limit:
        await safe_send(message.channel, 'There are only '+str(number_sign_ups)+' players signed up for the battle. We need at least '+str(battle_upper_limit)+' players to start.')
        return

    battle_info['reg_open'] = False
    current_players = []

    while len(current_players) < battle_upper_limit:

        battle_info['player_pools'] = init_player_pools(battle_info)

        valid_players = battle_info['player_pools']['valid_pool'] 

        while len(valid_players) > 0 and len(current_players) < battle_upper_limit:
            index = random.randint(0, len(valid_players) - 1) 
            removed_item = valid_players.pop(index)
            battle_info['sign_ups'].remove(removed_item)
            current_players.append(removed_item)  

        if len(current_players) < battle_upper_limit:

            past_players = battle_info['past_players']
            past_players.pop(0)
            battle_info['past_players'] = past_players


    battle_info['current_players'] = current_players
    battle_info['player_pools']['valid_pool'] = valid_players

    await safe_send(message.channel, 'Registration ended')

    final_string = '**PLAYERS IN XP BATTLE:**'
    index = 1
    for player_id in current_players:

        user = user_exists(db, player_id)
        user_display = get_battle_user_display(user, context)
        final_string += '\n'+str(index)+'. '+user_display+' | '+'<@'+str(user['discord_id'])+'>'

        index += 1

    guild = await get_guild(client)
    battle_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)
    await safe_send(message.channel, final_string)
    public_message = await safe_send(battle_channel, final_string)
    battle_info['players_msg'] = public_message.id

    set_constant_value(db, battle_constant_name, battle_info)