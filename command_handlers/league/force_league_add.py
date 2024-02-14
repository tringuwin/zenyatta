
from api import give_role
from discord_actions import get_role_by_id
from league import update_team_info
from user import get_league_team, user_exists
import constants


async def force_league_add_handler(db, message, client):

    mentioned_user = message.mentions[0]
    if not mentioned_user:
        await message.channel.send('no mentioned user')
        return
    
    word_parts = message.content.split()
    if len(word_parts) != 3:
        await message.channel.send('incorrect num of params')
        return
    
    team_name_to_join = word_parts[2]
    
    user = user_exists(db, mentioned_user.id)
    if not user:
        await message.channel.send('user not reg')
        return
    
    user_league_team = get_league_team(user)
    if user_league_team != "None":
        await message.channel.send('You are already on a league team. Please leave that team before joining another team.')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_team": team_name_to_join}})

    league_teams = db['leagueteams']
    league_team = league_teams.find_one({'team_name': team_name_to_join})

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