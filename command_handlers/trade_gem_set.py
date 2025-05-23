

from common_messages import not_registered_response
from rewards import change_tokens
from user.user import get_user_gems, user_exists
import constants

async def trade_gem_set_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_gems = get_user_gems(user)
    for color in constants.DEFAULT_GEMS:
        if user_gems[color] < 1:
            await message.channel.send('You do not have 1 of each gem color. You can only use this command if you have at least one of each.')
            return
        
    for color in user_gems:
        user_gems[color] -= 1

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {'gems': user_gems}})
    await change_tokens(db, user, 1000, 'trade-gem-set')

    await message.channel.send('Success! You traded in 1 of each Gem for 1,000 Tokens!')