
from common_messages import not_registered_response
from safe_send import safe_send
from user.user import get_gem_offer, user_exists


async def deny_gem_trade_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    gem_offer = get_gem_offer(user)
    if not gem_offer:
        await safe_send(message.channel, 'You do not have any gem trade offers at the moment.')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"gem_offer": None}})

    await safe_send(message.channel, 'You have denied the gem trade offer.')

