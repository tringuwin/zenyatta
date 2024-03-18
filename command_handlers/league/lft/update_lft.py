

from command_handlers.lft import get_lft_user
from common_messages import not_registered_response
from user import user_exists


async def update_lft_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    was_created, lft_user = get_lft_user(db, message.author, user)

    if was_created:
        await message.channel.send('LFT Profile was updated.')
        return
    
    avatar = message.author.display_avatar
    avatar_link = ''
    if avatar:
        avatar_link = avatar.url
    
    lft_users = db['lft_users']
    lft_users.update_one({"user_id": lft_user['user_id']}, {"$set": {"image_link": avatar_link}})

    await message.channel.send('LFT Profile was updated.')