
from common_messages import invalid_number_of_params
from helpers import make_string_from_word_list
from league import update_team_info, validate_admin
import constants

async def change_role_handler(db, message, client):

    word_list = message.content.split()
    if len(word_list) < 3:
        await invalid_number_of_params(message)
        return
    
    if len(message.mentions) < 1:
        await message.channel.send('Please mention the player to change their role.')
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
    for member in team_members:
        if member['discord_id'] == member_to_find.id:
            at_member = member
            at_member_index = cur_index
            break
        cur_index += 1

    if not at_member:
        await message.channel.send('That member is not part of your team.')
        return
    
    new_role = make_string_from_word_list(word_list, 2)
    
    my_team['members'][at_member_index]['role'] = new_role
    league_teams = db['leagueteams']
    league_teams.update_one({'team_name': team_name}, {"$set": {"members": my_team['members']}})

    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)
    await league_notifs_channel.send('Team Update for '+team_name+": "+member_to_find.mention+"'s role has been changed to "+new_role)

    await update_team_info(client, my_team)

    await message.channel.send("User's role was successfully updated.")