

from command_handlers.league.update_team import update_team
from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from helpers import can_be_int, valid_number_of_params
from league import validate_admin
from safe_send import safe_send


async def league_order_handler(db, message, client, context):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    valid_admin, team, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await safe_send(message.channel, 'You are not an admin of a league team.')
        return

    first_spot = params[1]
    if not can_be_int(first_spot):
        await safe_send(message.channel, first_spot+' is not a number')
        return
    first_spot = int(first_spot)
    
    second_spot = params[2]
    if not can_be_int(second_spot):
        await safe_send(message.channel, second_spot+' is not a number')
        return
    second_spot = int(second_spot)
    
    team_members = team['members']
    team_length = len(team_members)
    
    if first_spot > team_length:
        await safe_send(message.channel, str(first_spot)+' is too high. There is only '+str(team_length)+' players on your team.')
        return
    
    if second_spot > team_length:
        await safe_send(message.channel, str(second_spot)+' is too high. There is only '+str(team_length)+' players on your team.')
        return
    
    if first_spot < 1:
        await safe_send(message.channel, str(first_spot)+' is invalid. It must be a positive number.')
        return
    
    if second_spot < 1:
        await safe_send(message.channel, str(second_spot)+' is invalid. It must be a positive number.')
        return
    
    first_spot -= 1
    second_spot -= 1

    hold_first = team_members[first_spot]
    team_members[first_spot] = team_members[second_spot]
    team_members[second_spot] = hold_first

    teams_db = get_league_teams_collection_from_context(db, context)
    teams_db.update_one({"team_name": team_name}, {"$set": {"members": team_members}})

    await safe_send(message.channel, 'Please wait... This may take a while...')

    await update_team(db, team_name, client, context)

    await safe_send(message.channel, team_name+' was updated.')