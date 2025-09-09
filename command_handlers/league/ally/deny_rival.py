

from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from helpers import valid_number_of_params
from league import validate_admin
from safe_send import safe_send


async def deny_rival_handler(db, message, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await safe_send(message.channel, 'You are not a team admin of a league team.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name_to_deny = params[1].lower()

    league_teams = get_league_teams_collection_from_context(db, context)

    my_team_obj = league_teams.find_one({'team_name': team_name})
    if not my_team_obj:
        await safe_send(message.channel, 'Something went very wrong...')
        return
    
    other_team_obj = league_teams.find_one({'name_lower': team_name_to_deny})
    if not other_team_obj:
        await safe_send(message.channel, 'I did not find any league teams with that name... Check the spelling of the team name.')
        return

    if not (other_team_obj['team_name'] in my_team_obj['rival_reqs']):
        await safe_send(message.channel, 'Your team does not have a Rival Request from '+other_team_obj['team_name'])
        return
    
    my_team_obj['rival_reqs'].remove(other_team_obj['team_name'])
    league_teams.update_one({'team_name': my_team_obj['team_name']}, {'$set': {'rival_reqs': my_team_obj['rival_reqs']}})

    # confirmation message
    await safe_send(message.channel, 'Rival Request successfully denied.')