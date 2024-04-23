

from command_handlers.league.update_team import update_team
from discord_actions import get_role_by_id
from league import validate_admin


async def prune_team_handler(db, message, client):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    await message.channel.send('Prune Team command is processing... (this might take a while)')
    
    await update_team(db, team_name, client, message)

    await message.channel.send(team_name+' was updated.')