
from command_handlers.lft import get_lft_user
from common_messages import not_registered_response
from user import user_exists
import constants

async def toggle_lft_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    was_created, lft_user = get_lft_user(db, message.author, user)

    lft_users = db['lft_users']
    new_is_on = True
    if was_created:
        lft_users.insert_one(lft_user)
    else:
        new_is_on = not lft_user['is_on']
        lft_users.update_one({"user_id": lft_user['user_id']}, {"$set": {"is_on": new_is_on}})

    if new_is_on:
        await message.channel.send(f'Looking For Team is now **ON**. You will appear in the list of players looking for a team here: {constants.WEBSITE_DOMAIN}/sol/lft')
    else:
        await message.channel.send('Looking For Team is now **OFF**. You will no longer appear on the list of players looking for a team')


