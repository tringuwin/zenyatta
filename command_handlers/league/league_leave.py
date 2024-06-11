

from api import remove_role
from common_messages import not_registered_response
from discord_actions import get_role_by_id
from league import update_team_info
from user import get_league_team, user_exists
import constants

async def league_leave_handler(db, message, client):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    league_team = get_league_team(user)
    if league_team == 'None':
        await message.channel.send('You are not currently on a League Team.')
        return
    
    league_teams = db['leagueteams']
    team_object = league_teams.find_one({'team_name': league_team})
    if not team_object:
        await message.channel.send('ERROR LEAVING TEAM: PLEASE CONTACT STAFF')
        return
    
    if team_object['owner_id'] == message.author.id:
        await message.channel.send('You cannot use this command because you own this team. Please contact the league commissioner to change ownership.')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_team": 'None'}})
    
    team_role_id = team_object['team_role_id']
    team_role = await get_role_by_id(client, team_role_id)
    await remove_role(message.author, team_role, 'League Leave')

    final_members = []
    for member in team_object['members']:
        if member['discord_id'] != user['discord_id']:
            final_members.append(member)

    league_teams.update_one({'team_name': team_object['team_name']}, {"$set": {"members": final_members}})
    team_object['members'] = final_members

    await update_team_info(client, team_object, db)

    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)
    await league_notifs_channel.send('User '+message.author.mention+' has left the team "'+team_object['team_name']+'".')

    await message.channel.send('You have successfully left the team "'+team_object['team_name']+'"')
    