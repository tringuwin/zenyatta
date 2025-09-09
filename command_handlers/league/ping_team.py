from context.context_helpers import get_league_teams_collection_from_context
from discord_actions import get_role_by_id
from league import validate_admin
from safe_send import safe_send


async def ping_team_handler(db, message, client, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    league_teams = get_league_teams_collection_from_context(db, context)
    team_object = league_teams.find_one({'team_name': team_name})
    team_role_id = team_object['team_role_id']
    team_role = await get_role_by_id(client, team_role_id)

    await safe_send(message.channel, team_role.mention, True)