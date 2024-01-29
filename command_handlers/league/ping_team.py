from discord_actions import get_role_by_id
from league import validate_admin


async def ping_team_handler(db, message, client):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    league_teams = db['leagueteams']
    team_object = league_teams.find_one({'team_name': team_name})
    team_role_id = team_object['team_role_id']
    team_role = await get_role_by_id(client, team_role_id)

    await message.channel.send(team_role.mention)