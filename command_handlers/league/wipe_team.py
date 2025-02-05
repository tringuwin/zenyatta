
from common_messages import invalid_number_of_params
from discord_actions import get_role_by_id
from helpers import valid_number_of_params
from league_helpers import get_league_teams_collection


TAKEOVER_USERS = [
    979526718186459206
]


async def wipe_team(db, message, client, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name = params[1]
    team_name_lower = team_name.lower()

    league_teams_collection = get_league_teams_collection(db, context)
    team = league_teams_collection.find_one({'name_lower': team_name_lower})
    if not team:
        await message.channel.send('There is no team with the name: '+team_name)
        return
    
    team_role_id = team['team_role_id']
    team_role = await get_role_by_id(client, team_role_id)
    for member in team_role.members:

        if not (member.id in TAKEOVER_USERS):
            await member.remove_roles(team_role)

    await message.channel.send('Team role removed from all users.')
