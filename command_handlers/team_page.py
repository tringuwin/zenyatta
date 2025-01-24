

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
import constants

async def team_page_handler(db, message): 

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name = params[1]
    lower_team_name = team_name.lower()

    league_teams = db['leagueteams']
    team = league_teams.find_one({'name_lower': lower_team_name})
    if not team:
        await message.channel.send('Could not find any league team with the name "'+str(team_name)+'"')
        return
    
    final_string = 'Click the link below to see the team page for '+team['team_name']
    final_string += '\n\n'+f'{constants.WEBSITE_DOMAIN}/sol/team/'+lower_team_name
    
    await message.channel.send(final_string)