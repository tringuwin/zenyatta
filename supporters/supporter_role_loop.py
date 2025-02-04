
import constants
from discord_actions import get_role_by_id


def user_has_custom_role(custom_roles, user_id):

    custom_role = custom_roles.find_one({'user_id': user_id})
    if custom_role:
        return True
    
    return False


async def supporter_role_loop(db, message, client):

    role = await get_role_by_id(client, constants.SUPPORTER_ROLE_ID)
    role_members = role.members

    supporter_users = []

    for member in role_members:
        supporter_users.append(member.id)

    custom_roles = db['custom_roles']
    for supporter_id in supporter_users:
        if not user_has_custom_role(custom_roles, supporter_id):
            await message.channel.send('user with id '+str(supporter_id)+' does not have a custom role')

    