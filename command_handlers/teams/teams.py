
from common_messages import not_registered_response
from teams import get_team_by_name
from user import user_exists


async def teams_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        not_registered_response(message)
        return
    
    team_names = user['teams']

    team_index = 1
    if len(team_names) == 0:
        await message.channel.send('You are not currently part of any teams.')
    else:
        output_string = '**YOUR TEAMS**\n'
        for team_name in team_names:
            team = await get_team_by_name(db, team_name)
            if team:
                output_string += str(team_index)+'. '+team_name+' : '+str(len(team['members']))+'/'+str(team['team_size'])+' Players\n'
                team_index += 1

        await message.channel.send(output_string)
