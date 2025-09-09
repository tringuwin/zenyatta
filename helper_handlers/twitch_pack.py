from helpers import generic_find_user
from rewards import change_packs
from safe_send import safe_send


async def twitch_pack_handler(client, db, message):

    word_parts = message.content.split(' ')
    if len(word_parts) != 2:
        await safe_send(message.channel, 'Invalid number of parameters.')
        return
    
    discord_username = word_parts[1]
    user = await generic_find_user(client, db, discord_username)
    if not user:
        await safe_send(message.channel, "I could not find that user. (Maybe they're not registered yet?)")
        return
    
    await change_packs(db, user, 1)
    await safe_send(message.channel, 'SOL Card Pack redemption successfully given to user!')