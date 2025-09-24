
from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from helpers import can_be_int, generic_find_user, valid_number_of_params
from league import validate_admin
from safe_send import safe_send


async def change_tpp_handler(db, message, client, context):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    is_admin, my_team, team_name, _ = await validate_admin(db, message, context)

    team_members = my_team['members']

    if not is_admin:
        await safe_send(message.channel, 'You are not an admin of this league team. Please ask the team owner to be an admin.')
        return
    
    user_mentioned = params[1]
    user_obj = await generic_find_user(client, db, user_mentioned)
    if not user_obj:
        await safe_send(message.channel, 'I could not find any user with that username/user id.')
        return

    at_member = None
    at_member_index = 0
    cur_index = 0

    for member in team_members:
        if member['discord_id'] == user_obj['discord_id']:
            at_member = member
            at_member_index = cur_index
            break
        cur_index += 1

    if not at_member:
        await safe_send(message.channel, 'That member is not part of your team.')
        return
    
    tpp_offer = params[2]
    if not can_be_int(tpp_offer):
        await safe_send(message.channel, 'TPP Value must be a number between 0 and 100')
        return
    
    tpp_offer = int(tpp_offer)
    if tpp_offer < 0 or tpp_offer > 100:
        await safe_send(message.channel, 'TPP Value must be a number between 0 and 100')
        return
    
    available_tpp = 100
    for member in team_members:
        if member['discord_id'] != at_member['discord_id']:
            available_tpp -= member['TPP']

    if available_tpp < tpp_offer:
        await safe_send(message.channel, 'There is not enough available TPP for this team. This team only has '+str(available_tpp)+' TPP available.')
        return
    
    my_team['members'][at_member_index]['TPP'] = tpp_offer
    league_teams = get_league_teams_collection_from_context(db, context)
    league_teams.update_one({'team_name': team_name}, {"$set": {"members": my_team['members']}})

    await safe_send(message.channel, "User's TPP was successfully updated.")
