

from command_handlers.slime import get_user_slimed
from user.user import get_user_gems, user_exists


async def revive_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await message.channel.send("You need to register first!")
        return
    
    user_slimed = get_user_slimed(user)
    if user_slimed:
        await message.channel.send("You have already been slimed. You cannot revive anyone unless you are revived first.")
        return

    if len(message.mentions) != 1:
        await message.channel.send("Please mention a single user to slime.")
        return
    
    mentioned_member = message.mentions[0]
    mentioned_user = user_exists(db, mentioned_member.id)
    if not mentioned_user:
        await message.channel.send("The mentioned user is not registered.")
        return
    
    mentioned_user_slimed = get_user_slimed(mentioned_user)
    if not mentioned_user_slimed:
        await message.channel.send("That user has not been slimed, so they don't need to be revived.")
        return
    
    if mentioned_member == message.author:
        await message.channel.send("You cannot revive yourself.")
        return
    
    user_gems = get_user_gems(user)
    white_gems = user_gems['white']
    if white_gems < 1:
        await message.channel.send("You need a white gem to revive someone.")
        return
    
    users = db['users']

    user_gems['white'] -= 1
    users.update_one({"discord_id": message.author.id}, {"$set": {"gems": user_gems}})

    users.update_one({"discord_id": mentioned_user['discord_id']}, {"$set": {"slimed": False}})

    await message.channel.send(f"{message.author.mention} has revived {mentioned_member.mention} by using a white gem!")