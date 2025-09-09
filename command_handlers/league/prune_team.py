

from command_handlers.league.update_team import update_team
from discord_actions import get_role_by_id
from league import validate_admin
from safe_send import safe_send


async def prune_team_handler(db, message, client, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await safe_send(message.channel, 'You are not an admin of a league team.')
        return

    await safe_send(message.channel, 'Prune Team command is processing... (this might take a while)')

    await update_team(db, team_name, client, context)

    await safe_send(message.channel, team_name+' was updated.')