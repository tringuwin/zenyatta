
from helpers import generic_find_user, valid_number_of_params
from user.user import get_user_lootboxes


async def give_lootbox_handler(db, message, client):
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await message.channel.send('Invalid params')
        return
    
    user_id = params[1]
    box_number = int(params[2])

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('User not found')
        return
    
    user_boxes = get_user_lootboxes(user)
    user_boxes.append(box_number)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"lootboxes": user_boxes}})

    await message.channel.send('Lootbox given')
    