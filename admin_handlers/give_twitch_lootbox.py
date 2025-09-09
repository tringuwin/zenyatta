

from helpers import generic_find_user, valid_number_of_params
from safe_send import safe_send
from user.user import get_sub_lootboxes


async def give_twitch_lootbox_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, 'Invalid params')
        return
    
    user_id = params[1]
    number_to_give = int(params[2])

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'User not found')
        return
    
    sub_boxes = get_sub_lootboxes(user)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"sub_lootboxes": sub_boxes+number_to_give}})

    await safe_send(message.channel, 'Lootboxes given')