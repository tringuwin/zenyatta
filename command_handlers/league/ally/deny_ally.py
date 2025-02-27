

from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from helpers import valid_number_of_params
from league import validate_admin


async def deny_ally_handler(db, message, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await message.channel.send('You are not a team admin of a league team.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name_to_deny = params[1].lower()

    league_teams = get_league_teams_collection_from_context(db, context)

    my_team_obj = league_teams.find_one({'team_name': team_name})
    if not my_team_obj:
        await message.channel.send('Something went very wrong...')
        return
    
    other_team_obj = league_teams.find_one({'name_lower': team_name_to_deny})
    if not other_team_obj:
        await message.channel.send('I did not find any league teams with that name... Check the spelling of the team name.')
        return

    if not (other_team_obj['team_name'] in my_team_obj['ally_reqs']):
        await message.channel.send('Your team does not have an Ally Request from '+other_team_obj['team_name'])
        return
    
    my_team_obj['ally_reqs'].remove(other_team_obj['team_name'])
    league_teams.update_one({'team_name': my_team_obj['team_name']}, {'$set': {'ally_reqs': my_team_obj['ally_reqs']}})

    # confirmation message
    await message.channel.send('Ally Request successfully denied.')