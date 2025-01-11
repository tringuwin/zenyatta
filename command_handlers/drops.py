

from common_messages import not_registered_response
from user import get_user_drop_boxes, user_exists


async def drops(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_drops = get_user_drop_boxes(user)

    await message.channel.send('<:spicy_drop:1327677388720701450> **'+str(user_drops)+'**')
