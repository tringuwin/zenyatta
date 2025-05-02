



from common_messages import invalid_number_of_params
from helpers import can_be_int, get_constant_value, set_constant_value, valid_number_of_params


async def set_tourney_team_score(db, message):

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
    
    team_score = command_parts[2]
    if not can_be_int(team_score):
        await message.channel.send(team_score+" is not an integer")
        return
    team_score = int(team_score)

    tourney_widget_data = get_constant_value(db, 'tourney_widget')

    team_score_key = 'team'+str(team_number)+'_score'

    tourney_widget_data[team_score_key] = team_score

    set_constant_value(db, 'tourney_widget', tourney_widget_data)

    await message.channel.send("Team "+str(team_number)+" score set to "+str(team_score))
