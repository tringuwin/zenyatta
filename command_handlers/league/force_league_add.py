
from api import give_role
from context.context_helpers import get_league_notifs_channel_from_context, get_league_teams_collection_from_context
from discord_actions import get_role_by_id
from helpers import get_league_emoji_from_team_name
from league import update_team_info
from safe_send import safe_send
from user.user import get_league_team_with_context, user_exists


async def force_league_add_handler(db, message, client, context):

    mentioned_user = message.mentions[0]
    if not mentioned_user:
        await safe_send(message.channel, 'no mentioned user')
        return
    
    word_parts = message.content.split()
    if len(word_parts) != 3:
        await safe_send(message.channel, 'incorrect num of params')
        return
    
    team_name_to_join = word_parts[2]
    
    user = user_exists(db, mentioned_user.id)
    if not user:
        await safe_send(message.channel, 'user not reg')
        return
    
    user_league_team = get_league_team_with_context(user, context)
    if user_league_team != "None":
        await safe_send(message.channel, 'That user is already on a league team.')
        return
    
    league_teams = get_league_teams_collection_from_context(db, context)
    league_team = league_teams.find_one({'team_name': team_name_to_join})
    real_team_name = league_team['team_name']

    users = db['users']
    update_obj = {"league_team": real_team_name} if context == 'OW' else {'rivals_league_team': real_team_name}
    users.update_one({"discord_id": user['discord_id']}, {"$set": update_obj})

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
        await give_role(mentioned_user, role, 'League Accept')

    await update_team_info(client, league_team, db, context)

    league_notifs_channel = get_league_notifs_channel_from_context(client, context)

    team_emoji_string = get_league_emoji_from_team_name(real_team_name)

    await safe_send(league_notifs_channel, team_emoji_string+' User '+mentioned_user.mention+' has joined the team "'+team_name_to_join+'".')
    await safe_send(message.channel, 'Added user to league team.')