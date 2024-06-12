

from helpers import can_be_int, get_constant_value, set_constant_value
import random

from user import user_exists

async def battle_no_show_handler(db, message):

    parts = message.content.split()
    if len(parts) != 2:
        await message.channel.send('Need 2 params')
        return
    
    user_num = parts[1]

    if not can_be_int(user_num):
        await message.channel.send(user_num+' is not a number')
        return
    
    user_num = int(user_num)

    if user_num > 9 or user_num < 1:
        await message.channel.send('Must be a number between 1 and 9')
        return
    real_index = user_num - 1
    
    battle_obj = get_constant_value(db, 'battle')

    if len(battle_obj['sign_ups']) == 0:
        battle_obj['current_players'][real_index] = -1
        set_constant_value(db, 'battle', battle_obj)
        await message.channel.send('No player, replacing with a bot.')
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

    set_constant_value(db, 'battle', battle_obj)

    user = user_exists(db, found_player)
    await message.channel.send('Replacing with player '+user['battle_tag'])

    final_string = '**PLAYERS IN XP BATTLE:**'
    index = 1
    for player_id in battle_obj['current_players']:

        user = user_exists(db, player_id)
        final_string += '\n'+str(index)+'. '+user['battle_tag']

        index += 1

    await message.channel.send(final_string)