

from common_messages import not_registered_response
from drops.open_spicy_drop.open_spicy_drop import open_spicy_drop
from user import get_user_drop_boxes, user_exists


async def open_drop(db, client, message):

    user = user_exists(db)
    if not user:
        await not_registered_response(message)
        return

    user_drops = get_user_drop_boxes(user)
    if user_drops < 1:
        await message.channel.send('You do not have any Spicy Drops right now. Use the command **!nextdrop** to see how close you are to the next one!')
        return

    new_drops = user_drops - 1
    users = db['users']
    users.update_one({'discord_id': user['discord_id']}, {'$set': {'drop_boxes': new_drops}})

    await open_spicy_drop(db, client, message, user)