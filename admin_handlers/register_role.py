

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


async def register_role(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    role_id = int(params[1])

    custom_roles = db['custom_roles']

    custom_roles.insert_one({
        'role_id': role_id,
        'user_id': 0,
    })

    await message.channel.send('Role added to roles db.')
