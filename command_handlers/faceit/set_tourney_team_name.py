

from common_messages import invalid_number_of_params
from helpers import can_be_int, get_constant_value, set_constant_value, valid_number_of_params


async def set_tourney_team_name(db, message):

    command_parts = message.content.split('|')

    if len(command_parts) != 3:
        await invalid_number_of_params(message)
        return
    
    team_number = command_parts[1]
    if not can_be_int(team_number):
        await message.answer(team_number+" is not an integer")
        return
    team_number = int(team_number)
    
    if team_number != 1 and team_number != 2:
        await message.answer("Team number must be either 1 or 2")
        return
    
    team_name = command_parts[2]

    tourney_widget_data = get_constant_value(db, 'tourney_widget')

    team_name_key = 'team'+str(team_number)

    tourney_widget_data[team_name_key] = team_name

    set_constant_value(db, 'tourney_widget', tourney_widget_data)

    await message.answer("Team "+str(team_number)+" name set to "+team_name)
