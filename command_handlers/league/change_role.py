
from common_messages import invalid_number_of_params
from context.context_helpers import get_league_notifs_channel_from_context, get_league_teams_collection_from_context
from discord_actions import get_guild, get_member_by_username
from helpers import generic_find_user, get_league_emoji_from_team_name, make_string_from_word_list
from league import update_team_info, validate_admin
from safe_send import safe_send
from user.user import user_exists

async def change_role_handler(db, message, client, context):

    word_list = message.content.split()
    if len(word_list) < 3:
        await invalid_number_of_params(message)
        return
    
    is_admin, my_team, team_name, _ = await validate_admin(db, message, context)
    team_members = my_team['members']

    if not is_admin:
        await safe_send(message.channel, 'You are not an admin of this league team. Please ask the team owner to be an admin.')
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
        await safe_send(message.channel, 'User not found.')
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
        await safe_send(message.channel, 'That member is not part of your team.')
        return
    
    new_role = make_string_from_word_list(word_list, 2)
    if len(new_role) > 20:
        await safe_send(message.channel, 'Roles must be 20 letters or less.')
        return
    
    my_team['members'][at_member_index]['role'] = new_role
    league_teams = get_league_teams_collection_from_context(db, context)
    league_teams.update_one({'team_name': team_name}, {"$set": {"members": my_team['members']}})

    league_notifs_channel = get_league_notifs_channel_from_context(client, context)

    team_emoji_string = get_league_emoji_from_team_name(team_name)

    if mentioned_member:
        await safe_send(league_notifs_channel, team_emoji_string+' Team Update for '+team_name+": "+mentioned_member.mention+"'s role has been changed to "+new_role)
    else:
        await safe_send(league_notifs_channel, team_emoji_string+' Team Update for '+team_name+": "+username+"'s role has been changed to "+new_role)


    await update_team_info(client, my_team, db, context)

    await safe_send(message.channel, "User's role was successfully updated.")