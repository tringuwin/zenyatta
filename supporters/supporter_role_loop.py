
import constants
from discord_actions import get_role_by_id


async def supporter_role_loop(message, client):

    role = await get_role_by_id(client, constants.SUPPORTER_ROLE_ID)
    role_members = role.members

    members_string = ''

    for member in role_members:
        members_string += '\n'+member.name

    await message.channel.send('role members:\n' +members_string)