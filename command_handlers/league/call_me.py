

from common_messages import not_registered_response
from context.context_helpers import get_call_from_context
from helpers import make_string_from_word_list
from user.user import user_exists


async def call_me_handler(db, message, context):
    
    call_me_text = make_string_from_word_list(message.content.split(), 1)

    if len(call_me_text) > 20:
        await message.channel.send('You can only send a max of 20 letters.')
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    users = db['users']
    call_field = get_call_from_context(context)
    users.update_one({'discord_id': user['discord_id']}, {'$set': {call_field: call_me_text}})

    await message.channel.send('Your preference has been saved.')