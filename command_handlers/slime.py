

from user import user_exists


async def slime_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await message.channel.send("You need to register first!")
        return
    
    if 'slimed' in user:
        await message.channel.send("You have already been slimed. You cannot slime anyone else.")
        return

    if len(message.mentions) != 1:
        await message.channel.send("Please mention a single user to slime.")
        return
    
    mentioned_member = message.mentions[0]
    mentioned_user = user_exists(db, mentioned_member.id)
    if not mentioned_user:
        await message.channel.send("The mentioned user is not registered.")
        return
    
    if 'slimed' in mentioned_user:
        await message.channel.send("That user has already been slimed.")
        return
    
    if mentioned_member == message.author:
        await message.channel.send("You cannot slime yourself.")
        return
    
    users = db['users']
    users.update_one({"discord_id": mentioned_user['discord_id']}, {"$set": {"slimed": True}})

    await message.channel.send(f"{message.author.mention} has slimed {mentioned_member.mention}!")

    

    
