

from api import give_role
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_role_by_id
from helpers import make_string_from_word_list
from league import remove_league_invite, update_team_info
from user import get_league_invites, get_league_team, user_exists
import constants

async def league_accept_handler(db, message, client):

    word_list = message.content.split()
    if len(word_list) < 2:
        await invalid_number_of_params(message)
        return

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_league_team = get_league_team(user)
    if user_league_team != "None":
        await message.channel.send('You are already on a league team. Please leave that team before joining another team.')
        return
    
    team_name_to_join = make_string_from_word_list(word_list, 1)
    user_invites = get_league_invites(user)

    found_team = False
    for invite in user_invites:
        if invite == team_name_to_join:
            found_team = True
            break

    if not found_team:
        await message.channel.send('You do not have a team invite from the team "'+team_name_to_join+'". Please check the spelling and capitalization of the team name.')
        return
    
    league_teams = db['leagueteams']
    league_team = league_teams.find_one({'team_name': team_name_to_join})

    if len(league_team['members']) >= 25:
        await message.channel.send('This League Team already has 25 players, which is the maximum allowed. Please contact an admin of this team if you think this is a mistake.')
        return
    
    remove_league_invite(user, team_name_to_join, db)
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_team": team_name_to_join}})


    league_team['members'].append(
        {
            'discord_id': user['discord_id'],
            'is_owner': False,
            'is_admin': False,
            'role': '[No Role Yet]',
            'TPP': 0,
        }
    )

    league_teams.update_one({'team_name': team_name_to_join}, {"$set": {"members": league_team['members']}})

    role = await get_role_by_id(client, league_team['team_role_id'])
    if role:
        await give_role(message.author, role, 'League Accept')

    await update_team_info(client, league_team, db)

    league_notifs_channel = client.get_channel(constants.TEAM_NOTIFS_CHANNEL)
    await league_notifs_channel.send('User '+message.author.mention+' has joined the team "'+team_name_to_join+'".')
    await message.channel.send('You have successfully joined this team!')


