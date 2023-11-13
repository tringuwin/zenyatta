
import constants
from discord_actions import get_guild
from user import get_league_invites, get_league_team, user_exists


async def validate_admin(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        return None, None, None, None
    
    user_team = get_league_team(user)
    if user_team == "None":
        return None, None, None, None

    league_teams = db['leagueteams']
    my_team = league_teams.find_one({'team_name': user_team})
    if not my_team:
        return None, None, None, None

    is_admin = False
    team_members = my_team['members']
    for member in team_members:
        if member['discord_id'] == user['discord_id'] and member['is_admin']:
            is_admin = True
            break

    is_owner = False
    if my_team['owner_id'] == user['discord_id']:
        is_owner = True

    return is_admin, my_team, my_team['team_name'], is_owner

async def update_team_info(client, team):

    team_message_id = team['team_info_msg_id']
    team_info_channel = client.get_channel(constants.TEAM_INFO_CHANNEL)

    info_message = await team_info_channel.fetch_message(team_message_id)

    final_string = '**'+team['team_name']+' Team Details**\nMembers:'

    guild = await get_guild(client)

    available_tpp = 100
    for member in team['members']:

        guild_member = await guild.fetch_member(member['discord_id'])
        member_string = '*User not found*'
        if guild_member:
            member_string = guild_member.mention

        member_string += ' : '+member['role']+' : '+str(member['TPP'])+' TPP'

        available_tpp -= member['TPP']
        final_string += '\n'+member_string

    final_string += '\n--------------------------\nAvailable TPP: '+str(available_tpp)

    await info_message.edit(content=final_string)


def remove_league_invite(user, team_name, db):

    league_invites = get_league_invites(user)
    final_invites = []

    for invite in league_invites:
        if invite != team_name:
            final_invites.append(invite)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_invites": final_invites}})


def user_admin_on_team(user_id, league_team):

    for member in league_team['members']:

        if member['discord_id'] == user_id:
            if member['is_admin']:
                return True
            else:
                return False

    return False
