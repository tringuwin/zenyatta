
from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
from league import update_team_info, validate_admin
from user import get_league_team, set_user_league_team, user_exists
import constants


async def change_tpp_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    if len(message.mentions) < 1:
        await message.channel.send('Please mention the player to change their TPP.')
        return
    
    is_admin, my_team, team_name, _ = await validate_admin(db, message)

    team_members = my_team['members']

    if not is_admin:
        await message.channel.send('You are not an admin of this league team. Please ask the team owner to be an admin.')
        return
    
    member_to_find = message.mentions[0]
    at_member = None
    at_member_index = 0
    cur_index = 0
    old_tpp = 0
    for member in team_members:
        if member['discord_id'] == member_to_find.id:
            at_member = member
            at_member_index = cur_index
            old_tpp = member['TPP']
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

    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)
    await league_notifs_channel.send('Team Update for '+team_name+": "+member_to_find.mention+"'s TPP has been updated from "+str(old_tpp)+' to '+str(tpp_offer))

    await update_team_info(client, my_team, db)

    await message.channel.send("User's TPP was successfully updated.")


    
    
