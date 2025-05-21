

from common_messages import not_registered_response
from user.user import get_twitch_username, get_user_drop_boxes, user_exists


async def drops(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    twitch_username = get_twitch_username(user)
    if twitch_username == '[not set]':
        await message.reply('Your twitch is not linked with this server! Please link it with this command: **!twitch UsernameHere**')
        return
    
    user_drops = get_user_drop_boxes(user)

    await message.reply('<:spicy_drop:1327677388720701450> **'+str(user_drops)+'**')
