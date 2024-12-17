
from common_messages import invalid_number_of_params
from discord_actions import get_guild, get_member_by_username
from helpers import generic_find_user, get_league_emoji_from_team_name, make_string_from_word_list
from league import update_team_info, validate_admin
import constants
from user import user_exists

async def change_role_handler(db, message, client, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    word_list = message.content.split()
    if len(word_list) < 3:
        await invalid_number_of_params(message)
        return
    
    is_admin, my_team, team_name, _ = await validate_admin(db, message)
    team_members = my_team['members']

    if not is_admin:
        await message.channel.send('You are not an admin of this league team. Please ask the team owner to be an admin.')
        return
    
    user_to_change_role = None
    mentioned_member = None
    username = None

    if len(message.mentions) == 1:
        user_to_change_role = user_exists(db, message.mentions[0].id)
        mentioned_member = message.mentions[0]
    else:
        username = word_list[1]
        user_to_change_role = await generic_find_user(client, db, username)
        mentioned_member = await get_member_by_username(client, username)
    
    if not user_to_change_role:
        await message.channel.send('User not found.')
        return

    at_member = None
    at_member_index = 0
    cur_index = 0
    for member in team_members:
        if member['discord_id'] == user_to_change_role['discord_id']:
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

    team_emoji_string = get_league_emoji_from_team_name(team_name)

    if mentioned_member:
        await league_notifs_channel.send(team_emoji_string+' Team Update for '+team_name+": "+mentioned_member.mention+"'s role has been changed to "+new_role)
    else:
        await league_notifs_channel.send(team_emoji_string+' Team Update for '+team_name+": "+username+"'s role has been changed to "+new_role)


    await update_team_info(client, my_team, db)

    await message.channel.send("User's role was successfully updated.")