from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from teams import get_team_by_name
from user import user_exists

async def get_active_teams(db, team_names):

    active_teams = []

    for team_name in team_names:
        team = await get_team_by_name(db, team_name)
        if team:
            active_teams.append(team)

    return active_teams


async def get_teams_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    user_id = int(params[1])
    user = user_exists(db, user_id)
    if not user:
        not_registered_response(message)
        return
    
    team_names = user['teams']

    active_teams = await get_active_teams(db, team_names)

    team_index = 1
    if len(active_teams) == 0:
        await message.channel.send('That user currently part of any teams.')
    else:
        output_string = '**USER TEAMS**\n'
        for team in active_teams:

            output_string += str(team_index)+'. '+team['team_name']+' : '+str(len(team['members']))+'/'+str(team['team_size'])+' Players\n'
            team_index += 1

        await message.channel.send(output_string)
