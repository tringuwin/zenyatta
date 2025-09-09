

from helpers import can_be_int, generic_find_user, valid_number_of_params
from rewards import change_packs
from safe_send import safe_send
from user.user import get_subcount, get_sub_lootboxes


async def sub_rewards_handler(client, db, message):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await safe_send(message.channel, 'Invalid number of params')
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find a matching user.')
        return
    
    await change_packs(db, user, 3)
    sub_boxes = get_sub_lootboxes(user)
    subcount = get_subcount(user)

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"sub_lootboxes": sub_boxes + 1, "subcount": subcount + 1}})

    await safe_send(message.channel, 'Gave user 3 Packs, a sub point, and a sub lootbox to the user.')


async def gift_rewards_handler(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await safe_send(message.channel, 'Invalid number of params')
        return
    
    user_id = params[1]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await safe_send(message.channel, 'Could not find a matching user.')
        return
    
    num_to_give = params[2]
    if not can_be_int(num_to_give):
        await safe_send(message.channel, num_to_give+' is not a number')
        return
    
    num_to_give = int(num_to_give)
    if num_to_give < 1:
        await safe_send(message.channel, 'Number of gifted rewards to give must be greater than 0')
        return
    
    await change_packs(db, user, int(3 * num_to_give))

    await safe_send(message.channel, 'Gave gifted sub rewards to the user.')