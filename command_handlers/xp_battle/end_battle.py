

from helpers import get_constant_value, set_constant_value


async def end_battle_handler(db, message):

    battle_info = get_constant_value(db, 'battle')

    battle_info['battle_on'] = False
    battle_info['reg_open'] = False

    players_in_battle = []
    for team_name in battle_info['current_teams']:
        team = battle_info['current_teams'][team_name]
        for user_id in team:
            players_in_battle.append(user_id)

    battle_info['past_players'].append(players_in_battle)

    set_constant_value(db, 'battle', battle_info)

    await message.channel.send('Battle ended.')
    