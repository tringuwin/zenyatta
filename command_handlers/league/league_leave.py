

from api import remove_role
from common_messages import not_registered_response
from context.context_helpers import get_league_notifs_channel_from_context, get_league_team_field_from_context, get_league_teams_collection_from_context
from discord_actions import get_role_by_id
from helpers import get_league_emoji_from_team_name
from league import update_team_info
from league_helpers.remove_member_admin_role import remove_member_admin_role
from safe_send import safe_send
from user.user import get_league_team_with_context, user_exists

async def league_leave_handler(db, message, client, context):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    league_team = get_league_team_with_context(user, context)
    if league_team == 'None':
        await safe_send(message.channel, 'You are not currently on a League Team.')
        return
    
    league_teams = get_league_teams_collection_from_context(db, context)
    team_object = league_teams.find_one({'team_name': league_team})
    if not team_object:
        await safe_send(message.channel, 'ERROR LEAVING TEAM: PLEASE CONTACT STAFF')
        return
    
    if team_object['owner_id'] == message.author.id:
        await safe_send(message.channel, 'You cannot use this command because you own this team. Please contact the league commissioner to change ownership.')
        return
    
    users = db['users']
    league_team_field = get_league_team_field_from_context(context)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {league_team_field: 'None'}})
    
    team_role_id = team_object['team_role_id']
    team_role = await get_role_by_id(client, team_role_id)
    await remove_role(message.author, team_role, 'League Leave')

    final_members = []
    was_admin = False
    for member in team_object['members']:
        if member['discord_id'] != user['discord_id']:
            final_members.append(member)
        else:
            was_admin = member['is_admin']

    league_teams.update_one({'team_name': team_object['team_name']}, {"$set": {"members": final_members}})
    team_object['members'] = final_members

    if was_admin:
        await remove_member_admin_role(message.author, context, client)

    await update_team_info(client, team_object, db, context)

    league_notifs_channel = get_league_notifs_channel_from_context(client, context)
    team_emoji_string = get_league_emoji_from_team_name(team_object['team_name'])
    await safe_send(league_notifs_channel, team_emoji_string+' User '+message.author.mention+' has left the team "'+team_object['team_name']+'".')

    await safe_send(message.channel, 'You have successfully left the team "'+team_object['team_name']+'"')
