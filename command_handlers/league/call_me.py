

from common_messages import not_registered_response
from helpers import make_string_from_word_list
from user import user_exists


async def call_me_handler(db, message, context):

    if context == 'MR':
        await message.channel.send('This command is not ready for Marvel Rivals yet.')
        return
    
    call_me_text = make_string_from_word_list(message.content.split(), 1)

    if len(call_me_text) > 20:
        await message.channel.send('You can only send a max of 20 letters.')
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    users = db['users']
    users.update_one({'discord_id': user['discord_id']}, {'$set': {'call': call_me_text}})

    await message.channel.send('Your preference has been saved.')