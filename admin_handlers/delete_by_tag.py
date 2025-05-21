
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from user.user import get_user_by_tag


async def delete_by_tag_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    lower_tag = params[1].lower()
    user = get_user_by_tag(db, lower_tag)
    if not user:
        await message.channel.send('There is no user with that battle tag.')
        return
    
    users = db['users']
    users.delete_one({'lower_tag': lower_tag})

    await message.channel.send('User with battle tag '+lower_tag+' has been deleted.')