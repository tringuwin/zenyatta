
from common_messages import not_registered_response
from user import get_lvl_info, user_exists


async def level_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    level, xp = get_lvl_info(user)
    await message.channel.send('You are level **'+str(level)+"**. XP required for next level: ("+str(xp)+"/"+str(level*100)+")")
    
