

from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context, get_league_url_from_context
from helpers import valid_number_of_params
import constants

async def team_page_handler(db, message, context): 

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name = params[1]
    lower_team_name = team_name.lower()

    league_teams = get_league_teams_collection_from_context(db, context)
    team = league_teams.find_one({'name_lower': lower_team_name})
    if not team:
        await message.channel.send('Could not find any league team with the name "'+str(team_name)+'"')
        return
    
    league_url = get_league_url_from_context(context)

    final_string = 'Click the link below to see the team page for '+team['team_name']
    final_string += '\n\n'+f'{constants.WEBSITE_DOMAIN}/{league_url}/team/'+lower_team_name
    
    await message.channel.send(final_string)