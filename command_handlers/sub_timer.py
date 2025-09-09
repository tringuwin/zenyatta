

from common_messages import not_registered_response
from safe_send import safe_send
from user.user import get_last_sub_box, user_exists
import time

import constants

async def sub_timer_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    last_sub_box = get_last_sub_box(user)

    current_time = time.time()
    difference = current_time - last_sub_box

    if difference >= constants.TIME_IN_30_DAYS:
        await safe_send(message.channel, 'Your next Twitch Sub Lootbox is ready as soon as you subscribe.')
    else:

        seconds_left = constants.TIME_IN_30_DAYS - difference
        days = round(seconds_left / 86400.0, 2)

        await safe_send(message.channel, 'Your next Twitch Sub Lootbox will be ready in '+str(days)+' days, if you are still subscribed at that time.')



    