from helpers import generic_find_user
from rewards import change_passes
from user import user_exists


async def twitch_pass_handler(client, db, message):

    word_parts = message.content.split(' ')
    if len(word_parts) != 2:
        await message.channel.send('Invalid number of parameters.')
        return
    
    discord_username = word_parts[1]
    user = await generic_find_user(client, db, discord_username)
    if not user:
        await message.channel.send("I could not find that user. (Maybe they're not registered yet?)")
        return
    
    await change_passes(db, user, 1)
    await message.channel.send('Priority Pass redemption successfully given to user!')