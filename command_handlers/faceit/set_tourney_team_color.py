



from common_messages import invalid_number_of_params
from helpers import can_be_int, get_constant_value, set_constant_value, valid_number_of_params


VALID_COLORS = [
    'neon',
    'yellow',
    'lime',
    'aqua',
    'orange',
    'brown',
    'magenta',
    'blue',
    'red',
    'gold',
    'green',
    'pink',
    'purple'
]

async def set_tourney_team_color(db, message):

    command_parts = message.content.split('|')

    if len(command_parts) != 3:
        await invalid_number_of_params(message)
        return
    
    team_number = command_parts[1]
    if not can_be_int(team_number):
        await message.channel.send(team_number+" is not an integer")
        return
    team_number = int(team_number)
    
    if team_number != 1 and team_number != 2:
        await message.channel.send("Team number must be either 1 or 2")
        return
    
    team_color = command_parts[2].lower()
    if team_color not in VALID_COLORS:
        await message.channel.send("Invalid color. Valid colors are: "+", ".join(VALID_COLORS))
        return

    tourney_widget_data = get_constant_value(db, 'tourney_widget')

    team_color_key = 'team'+str(team_number)+'_color'

    tourney_widget_data[team_color_key] = team_color

    set_constant_value(db, 'tourney_widget', tourney_widget_data)

    await message.channel.send("Team "+str(team_number)+" color set to "+team_color)
