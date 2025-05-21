

from common_messages import not_registered_response
from user.user import get_twitch_username, get_user_minute_points, user_exists


async def next_drop(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    twitch_username = get_twitch_username(user)
    if twitch_username == '[not set]':
        await message.reply('Your twitch is not linked with this server! Please link it with this command: **!twitch UsernameHere**')
        return
    
    minute_points = get_user_minute_points(user)

    percent = minute_points * 10

    final_string = 'Your next <:spicy_drop:1327677388720701450> Spicy Drop is '+str(percent)+'% ready! Just watch **'+str(10-minute_points)+' minutes** on one of our official twitch channels to claim it!'
    final_string += '\n\n'

    boxes_left = 10
    while boxes_left > 0:

        if minute_points > 0:
            final_string += '🟩'
            minute_points -= 1
        else:
            final_string += '⬜'


        boxes_left -= 1

    await message.reply(final_string)