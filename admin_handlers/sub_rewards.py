

from helpers import generic_find_user, valid_number_of_params
from rewards import change_packs, change_pp
from user import get_sub_lootboxes


async def sub_rewards_handler(client, db, message):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await message.channel.send('Invalid number of params')
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('Could not find a matching user.')
        return
    
    await change_packs(db, user, 3)
    await change_pp(db, user, 300)
    sub_boxes = get_sub_lootboxes(user)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"sub_lootboxes": sub_boxes + 1}})

    await message.channel.send('Gave user 3 Packs, 300 XP and a sub lootbox to the user.')