

from safe_send import safe_send
from user.user import get_user_slimed, user_exists

async def slime_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await safe_send(message.channel, "You need to register first!")
        return
    
    user_slimed = get_user_slimed(user)
    if user_slimed:
        await safe_send(message.channel, "You have already been slimed. You cannot slime anyone else unless you are revived first.")
        return

    if len(message.mentions) != 1:
        await safe_send(message.channel, "Please mention a single user to slime.")
        return
    
    mentioned_member = message.mentions[0]
    mentioned_user = user_exists(db, mentioned_member.id)
    if not mentioned_user:
        await safe_send(message.channel, "The mentioned user is not registered.")
        return
    
    mentioned_user_slimed = get_user_slimed(mentioned_user)
    if mentioned_user_slimed:
        await safe_send(message.channel, "That user has already been slimed.")
        return
    
    if mentioned_member == message.author:
        await safe_send(message.channel, "You cannot slime yourself.")
        return
    
    users = db['users']
    users.update_one({"discord_id": mentioned_user['discord_id']}, {"$set": {"slimed": True}})

    await safe_send(message.channel, f"{message.author.mention} has slimed {mentioned_member.mention}!")

    
