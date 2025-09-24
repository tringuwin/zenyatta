
from context.context_helpers import get_league_notifs_channel_from_context, get_league_teams_collection_from_context
from discord_actions import get_guild
from helpers import get_league_emoji_from_team_name
from league import user_admin_on_team, validate_admin
from league_helpers.give_member_admin_role import give_member_admin_role
from safe_send import safe_send
from user.user import get_league_team_with_context, user_exists



async def make_team_admin_handler(db, message, client, context):

    _, _, team_name, is_owner = await validate_admin(db, message, context)

    if not is_owner:
        await safe_send(message.channel, 'You are not the owner of a league team.')
        return
    
    if len(message.mentions) < 1:
        await safe_send(message.channel, 'Please mention the user to make then an admin.')
        return
    
    mentioned_member = message.mentions[0]
    
    user = user_exists(db, mentioned_member.id)
    if not user:
        await safe_send(message.channel, 'That user is not registered yet.')
        return
    
    user_league_team = get_league_team_with_context(user, context)
    if user_league_team != team_name:
        await safe_send(message.channel, 'That user is not on your team.')
        return
    
    league_teams = get_league_teams_collection_from_context(db, context)
    team_object = league_teams.find_one({'team_name': team_name})
    if not team_object:
        await safe_send(message.channel, 'Team was not found.')
        return
    
    if user_admin_on_team(mentioned_member.id, team_object):
        await safe_send(message.channel, 'That user is already on admin on your team.')
        return
    
    new_members = team_object['members']
    for member in new_members:
        if member['discord_id'] == mentioned_member.id:
            member['is_admin'] = True

    league_teams.update_one({'team_name': team_name}, {"$set": {"members": new_members}})

    await give_member_admin_role(mentioned_member, context, client)

    league_notifs_channel = get_league_notifs_channel_from_context(client, context)
    team_emoji_string = get_league_emoji_from_team_name(team_name)
    await safe_send(league_notifs_channel, team_emoji_string+' Team Update for '+team_name+": "+mentioned_member.mention+" is now a team admin.")

    team_object['members'] = new_members
    await update_team_info(client, team_object, db, context)

    await safe_send(message.channel, 'User was made an admin of your league team')

