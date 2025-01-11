

from common_messages import not_registered_response
from user import get_twitch_username, get_user_minute_points, user_exists


async def next_drop(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    twitch_username = get_twitch_username(user)
    if twitch_username == '[not set]':
        await message.channel.send('Your twitch is not linked with this server! Please link it with this command: **!twitch UsernameHere**')
        return
    
    minute_points = get_user_minute_points(user)

    percent = minute_points * 10

    await message.channel.send('Your next Spicy Drop is '+str(percent)+'% ready! Just watch **'+str(10-minute_points)+' minutes** on one of our official twitch channels to claim it!')