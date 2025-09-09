from helpers import make_string_from_word_list
from safe_send import safe_send
from user.user import user_exists

async def address_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await safe_send(message.channel, "You are not registered yet. Please register first.")
        return

    user_address = make_string_from_word_list(message.content.split(), 1)
    
    users = db['users']
    users.update_one({'discord_id': message.author.id}, {'$set': {'address': user_address}})

    await safe_send(message.channel, 'Your address has been added successfully!')