

from helpers import get_constant_value, set_constant_value
from xp_battles import init_player_pools
import random

async def end_reg_handler(db, message):

    battle_info = get_constant_value(db, 'battle')

    number_sign_ups = len(battle_info['sign_ups'])
    if number_sign_ups < 9:
        await message.channel.send('There are only '+str(number_sign_ups)+' players signed up for the battle. We need at least 9 players to start.')
        return
    
    player_pools = init_player_pools(battle_info)

    battle_info['player_pools'] = player_pools
    battle_info['reg_open'] = False

    valid_players = battle_info['player_pools']['valid_pool'] 
    current_players = []

    while len(valid_players) > 0 and len(current_players) < 9:
        index = random.randint(0, len(valid_players) - 1) 
        removed_item = valid_players.pop(index)
        current_players.append(removed_item)  


    # while len(current_players) < 9:

    battle_info['current_players'] = current_players
    battle_info['player_pools']['valid_pool'] = valid_players

    set_constant_value(db, 'battle', battle_info)

    await message.channel.send('Registration ended')