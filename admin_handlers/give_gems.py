
from common_messages import invalid_number_of_params
from helpers import generic_find_user, valid_number_of_params
from safe_send import safe_send
from user.user import get_user_gems


async def give_gems_handler(db, message, client):
    
    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user_id = params[1]
    color = params[2].lower()
    num = int(params[3])

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find that user.')
        return
    
    user_gems = get_user_gems(user)
    user_gems[color] += num

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}})

    await safe_send(message.channel, 'Gems given')