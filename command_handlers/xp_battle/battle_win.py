

from common_messages import invalid_number_of_params
from helpers import get_constant_value, set_constant_value, valid_number_of_params


async def battle_win_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_winner = params[1].lower()
    if team_winner != 'red' and team_winner != 'blue' and team_winner != 'tie':
        await message.channel.send('Invalid team name. Must be red or blue.')
        return

    battle_info = get_constant_value(db, 'battle')

    players_in_battle = []
    for team_name in battle_info['current_teams']:
        team = battle_info['current_teams'][team_name]
        for user_id in team:
            players_in_battle.append(user_id)

    battle_info['past_players'].append(players_in_battle)

    set_constant_value(db, 'battle', battle_info)

    await message.channel.send('Winner recorded and battle ended.')
