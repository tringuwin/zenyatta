from helpers import generic_find_user
from rewards import change_packs


async def twitch_pack_handler(client, db, message):

    word_parts = message.content.split(' ')
    if len(word_parts) != 2:
        await message.channel.send('Invalid number of parameters.')
        return
    
    discord_username = word_parts[1]
    user = await generic_find_user(client, db, discord_username)
    if not user:
        await message.channel.send("I could not find that user. (Maybe they're not registered yet?)")
        return
    
    await change_packs(db, user, 1)
    await message.channel.send('SOL Card Pack redemption successfully given to user!')