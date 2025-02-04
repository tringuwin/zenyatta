
from api import get_member, give_role
import constants
from discord_actions import get_guild, get_role_by_id


def user_has_custom_role(custom_roles, user_id):

    custom_role = custom_roles.find_one({'user_id': user_id})
    if custom_role:
        return True
    
    return False


async  def assign_custom_role(client, custom_roles, user_id):

    empty_custom_role = custom_roles.find_one({'user_id': 0})
    if not empty_custom_role:
        raise Exception('No available custom roles, please register more.')

    custom_role = get_role_by_id(client, empty_custom_role['role_id'])
    if not custom_role:
        raise Exception('Could not find custom role with id of: '+str(empty_custom_role['role_id']))
    
    guild = await get_guild(client)
    member = get_member(guild, user_id, 'Assign Custom Role')
    if not member:
        raise Exception('User with id '+str(user_id)+' said to be a supporter, but not found in the server.')
    
    await give_role(member, custom_role, 'Assign Custom Role')
    custom_roles.update_one({'role_id': empty_custom_role['role_id']}, {'$set': {'user_id': user_id}})


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
            await assign_custom_role(client, custom_roles, supporter_id)


    