



from api import remove_role
from context.context_helpers import get_team_admin_role_id_from_context
from discord_actions import get_guild


async def remove_member_admin_role(member, context, client):

    admin_role_id = get_team_admin_role_id_from_context(context)

    guild = await get_guild(client)
    admin_role = guild.get_role(admin_role_id)

    await remove_role(member, admin_role, 'Remove Admin Role')