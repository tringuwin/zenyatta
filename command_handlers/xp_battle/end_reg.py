

from discord_actions import get_guild
from helpers import get_constant_value, set_constant_value
from user import user_exists
from xp_battles import init_player_pools
import random
import constants

async def end_reg_handler(db, message, client):

    battle_info = get_constant_value(db, 'battle')

    if not battle_info['battle_on']:
        await message.channel.send('There is no battle right now.')
        return    
    
    if not battle_info['reg_open']:
        await message.channel.send('Registration is not open for this battle right now.')
        return

    number_sign_ups = len(battle_info['sign_ups'])
    if number_sign_ups < 9:
        await message.channel.send('There are only '+str(number_sign_ups)+' players signed up for the battle. We need at least 9 players to start.')
        return

    battle_info['reg_open'] = False
    current_players = []

    while len(current_players) < 9:

        battle_info['player_pools'] = init_player_pools(battle_info)

        valid_players = battle_info['player_pools']['valid_pool'] 

        while len(valid_players) > 0 and len(current_players) < 9:
            index = random.randint(0, len(valid_players) - 1) 
            removed_item = valid_players.pop(index)
            battle_info['sign_ups'].remove(removed_item)
            current_players.append(removed_item)  

        if len(current_players) < 9:

            past_players = battle_info['past_players']
            past_players.pop(0)
            battle_info['past_players'] = past_players



    battle_info['current_players'] = current_players
    battle_info['player_pools']['valid_pool'] = valid_players

    await message.channel.send('Registration ended')

    final_string = '**PLAYERS IN XP BATTLE:**'
    index = 1
    for player_id in current_players:

        user = user_exists(db, player_id)
        final_string += '\n'+str(index)+'. '+user['battle_tag']

        index += 1

    guild = await get_guild(client)
    battle_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)
    await message.channel.send(final_string)
    public_message = await battle_channel.send(final_string)
    battle_info['players_msg'] = public_message.id

    set_constant_value(db, 'battle', battle_info)