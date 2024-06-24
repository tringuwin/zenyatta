

from helpers import can_be_int, generic_find_user, valid_number_of_params
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

    await message.channel.send('Gave user 3 Packs, 300 PP and a sub lootbox to the user.')


async def gift_rewards_handler(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await message.channel.send('Invalid number of params')
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('Could not find a matching user.')
        return
    
    num_to_give = params[2]
    if not can_be_int(num_to_give):
        await message.channel.send(num_to_give+' is not a number')
        return
    
    num_to_give = int(num_to_give)
    if num_to_give < 1:
        await message.channel.send('Number of gifted rewards to give must be greater than 0')
        return
    
    await change_packs(db, user, int(3 * num_to_give))
    await change_pp(db, user, int(300 * num_to_give))

    await message.channel.send('Gave gifted sub rewards to the user.')