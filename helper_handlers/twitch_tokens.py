from rewards import change_tokens
from user import user_exists


async def twitch_tokens_handler(db, message, num):

    word_parts = message.content.split(' ')
    if len(word_parts) != 2:
        await message.channel.send('Invalid number of parameters.')
        return
    
    if len(message.mentions) != 1:
        await message.channel.send('Please mention 1 person for this redemption.')
        return
    
    mention = message.mentions[0]
    user = user_exists(db, mention.id)
    if not user:
        await message.channel.send("I could not find that user. (Maybe they're not registered yet?)")
        return
    
    await change_tokens(db, user, num)
    await message.channel.send('Token redemption successfully given to user!')
    