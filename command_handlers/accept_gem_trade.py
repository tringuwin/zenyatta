
from common_messages import not_registered_response
from user import get_gem_offer, get_user_gems, user_exists


async def accept_gem_trade_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    gem_offer = get_gem_offer(user)
    if not gem_offer:
        await message.channel.send('You do not currently have any gem offers at this time.')
        return
    
    other_user_id = gem_offer['sender_id']
    other_user = user_exists(db, other_user_id)
    if not other_user:
        await message.channel.send("There was an error finding your trade partner's data.")
        return
    
    users = db['users']

    user_gems = get_user_gems(user)
    color_to_give = gem_offer['sender_wants']
    color_owned = user_gems[color_to_give]
    if color_owned < 1:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"gem_offer": None}})
        await message.channel.send('You no longer have any '+color_to_give+' gems. This offer has been cancelled.')
        return
    
    sender_gems = get_user_gems(other_user)
    color_to_get = gem_offer['sender_offer']
    other_color_owned = sender_gems[color_to_get]
    if other_color_owned < 1:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"gem_offer": None}})
        await message.channel.send('The other user no longer has any '+color_to_get+' gems. This offer has been cancelled.')
        return
    
    user_gems[color_to_give] -= 1
    user_gems[color_to_get] += 1
    sender_gems[color_to_get] -= 1
    sender_gems[color_to_give] += 1

    users.update_one({"discord_id": user['discord_id']}, {"$set": {"gem_offer": None, "gems": user_gems}})
    users.update_one({"discord_id": other_user['discord_id']}, {"$set": {"gems": sender_gems}})

    await message.channel.send('Gem trade complete!')
    
