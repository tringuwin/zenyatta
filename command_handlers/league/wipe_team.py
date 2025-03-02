
from common_messages import invalid_number_of_params
from context.context_helpers import get_league_teams_collection_from_context
from discord_actions import get_role_by_id
from helpers import valid_number_of_params


TAKEOVER_USERS = [
    979526718186459206, # ragu tester
    340644170656120833 # adam silver
]


async def remove_team_role_from_all_members(message, team, client):

    team_role_id = team['team_role_id']
    team_role = await get_role_by_id(client, team_role_id)
    for member in team_role.members:

        if not (member.id in TAKEOVER_USERS):
            await member.remove_roles(team_role)

    await message.channel.send('Team role removed from all users.')


async def clear_members_from_league_team(message, league_teams_collection, team):

    final_members = []

    for member in team['members']:
        if member['discord_id'] in TAKEOVER_USERS:
            final_members.append(member)

    league_teams_collection.update_one({'team_name': team['team_name']}, {'$set': {'members': final_members}})

    await message.channel.send('All members removed from team object.')



async def remove_league_team_from_all_users(message, db, team):

    users = db['users']

    users_with_team = users.find({'league_team': team['team_name']})
    for user in users_with_team:
        if not (user['discord_id'] in TAKEOVER_USERS):
            users.update_one({'discord_id': user['discord_id']}, {'$set': {'league_team': 'None'}})

    await message.channel.send('All users with league team cleared.')


async def wipe_team(db, message, client, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name = params[1]
    team_name_lower = team_name.lower()

    league_teams_collection = get_league_teams_collection_from_context(db, context)
    team = league_teams_collection.find_one({'name_lower': team_name_lower})
    if not team:
        await message.channel.send('There is no team with the name: '+team_name)
        return
    
    await remove_team_role_from_all_members(message, team, client)
    await clear_members_from_league_team(message, league_teams_collection, team)
    await remove_league_team_from_all_users(message, db, team)
