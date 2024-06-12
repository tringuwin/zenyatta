

from helpers import get_constant_value, set_constant_value
import random

from user import user_exists


async def battle_teams_handler(db, message):

    battle_info = get_constant_value(db, 'battle')

    if not battle_info['battle_on']:
        await message.channel.send('There is no battle right now.')
        return

    current_players = battle_info['current_players']

    blue_team = []
    red_team = []
    
    spicy_team = random.choice(['blue', 'red'])
    first_user = current_players.pop(0)
    if spicy_team == 'blue':
        blue_team.append(1112204092723441724)
        red_team.append(first_user)
    else:
        red_team.append(1112204092723441724)
        blue_team.append(first_user)

    is_blue = True
    while len(current_players) > 0:
        index = random.randint(0, len(current_players) - 1) 
        removed_user = current_players.pop(index)

        if is_blue:
            blue_team.append(removed_user)
        else:
            red_team.append(removed_user)

        is_blue = not is_blue

    battle_info['current_teams'] = {
        'blue': blue_team,
        'red': red_team
    }

    set_constant_value(db, 'battle', battle_info)

    final_string = '**BLUE TEAM:**'
    user_index = 0
    for user_id in blue_team:
        user = user_exists(db, user_id)
        final_string += '\n'+str(user_index)+'. '+user['battle_tag']

        user_index += 1

    final_string += '\n\n**RED TEAM:**'
    user_index = 0
    for user_id in red_team:
        if user_id == -1:
            final_string += '\n'+'BOT 🤖'
        else:
            user = user_exists(db, user_id)
            final_string += '\n'+str(user_index)+'. '+user['battle_tag']

        user_index += 1
        
    await message.channel.send(final_string)

