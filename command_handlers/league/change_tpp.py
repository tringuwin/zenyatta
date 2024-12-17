
from common_messages import invalid_number_of_params
from helpers import can_be_int, generic_find_user, valid_number_of_params
from league import update_team_info, validate_admin


async def change_tpp_handler(db, message, client, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    is_admin, my_team, team_name, _ = await validate_admin(db, message)

    team_members = my_team['members']

    if not is_admin:
        await message.channel.send('You are not an admin of this league team. Please ask the team owner to be an admin.')
        return
    
    user_mentioned = params[1]
    user_obj = await generic_find_user(client, db, user_mentioned)
    if not user_obj:
        await message.channel.send('I could not find any user with that username/user id.')
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
        await message.channel.send('That member is not part of your team.')
        return
    
    tpp_offer = params[2]
    if not can_be_int(tpp_offer):
        await message.channel.send('TPP Value must be a number between 0 and 100')
        return
    
    tpp_offer = int(tpp_offer)
    if tpp_offer < 0 or tpp_offer > 100:
        await message.channel.send('TPP Value must be a number between 0 and 100')
        return
    
    available_tpp = 100
    for member in team_members:
        if member['discord_id'] != at_member['discord_id']:
            available_tpp -= member['TPP']

    if available_tpp < tpp_offer:
        await message.channel.send('There is not enough available TPP for this team. This team only has '+str(available_tpp)+' TPP available.')
        return
    
    my_team['members'][at_member_index]['TPP'] = tpp_offer
    league_teams = db['leagueteams']
    league_teams.update_one({'team_name': team_name}, {"$set": {"members": my_team['members']}})

    await update_team_info(client, my_team, db)

    await message.channel.send("User's TPP was successfully updated.")


    
    
