

from helpers import get_constant_value, set_constant_value
from xp_battles import init_player_pools


async def end_reg_handler(db, message):

    battle_info = get_constant_value(db, 'battle')

    number_sign_ups = len(battle_info['sign_ups'])
    if number_sign_ups < 9:
        await message.channel.send('There are only '+str(number_sign_ups)+' players signed up for the battle. We need at least 9 players to start.')
        return
    
    player_pools = init_player_pools(battle_info)

    battle_info['player_pools'] = player_pools
    battle_info['reg_open'] = False

    current_players = []
    
    set_constant_value(db, 'battle', battle_info)

    await message.channel.send('Registration ended')