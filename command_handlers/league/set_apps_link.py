

from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from helpers import valid_number_of_params
from league import validate_admin

async def set_apps_link_handler(db, message, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    apps_link = params[1]

    team_name_lower = team_name.lower()

    league_teams = get_league_teams_collection_from_context(db, context)
    my_team = league_teams.find_one({'name_lower': team_name_lower})
    if not my_team:
        await message.channel.send('Was not able to set the application for this team because this team is not yet listed on the application website. If you think this is a mistake please contact the server owner.')
        return

    my_team['applications']['appsLink'] = apps_link

    league_teams.update_one({"name_lower": team_name_lower}, {"$set": {"applications": my_team['applications']}})
    await message.channel.send('Application link for '+team_name+' has been updated.')
    