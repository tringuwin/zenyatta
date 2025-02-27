from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from helpers import valid_number_of_params
from league import validate_admin


async def rival_request_handler(db, message, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await message.channel.send('You are not a team admin of a league team.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name_to_req = params[1].lower()

    if team_name.lower() == team_name_to_req:
        await message.channel.send('You cannot send a Rival Request to your own team.')
        return

    league_teams = get_league_teams_collection_from_context(db, context)

    my_team_obj = league_teams.find_one({'team_name': team_name})
    if not my_team_obj:
        await message.channel.send('Something went very wrong...')
        return
    
    other_team_obj = league_teams.find_one({'name_lower': team_name_to_req})
    if not other_team_obj:
        await message.channel.send('I did not find any league teams with that name... Check the spelling of the team name.')
        return

    # is already sent rival request
    if team_name in other_team_obj['rival_reqs']:
        await message.channel.send('This team already has a Rival Request from '+team_name+'.')
        return

    # is already rival
    if team_name in other_team_obj['rivals']:
        await message.channel.send('This team is already a Rival of '+team_name+'.')
        return

    # is already ally
    if team_name in other_team_obj['allies']:
        await message.channel.send('This team is currently an Ally of '+team_name+'. Remove them as an Ally to send a Rival request.')
        return

    # add rival request to the other teams requests
    other_team_obj['rival_reqs'].append(team_name)
    league_teams.update_one({'name_lower': team_name_to_req}, {'$set': {'rival_reqs': other_team_obj['rival_reqs']}})

    # confirmation message
    await message.channel.send('You have successfully sent an Rival Request from '+team_name+' to '+other_team_obj['team_name']+'!')
