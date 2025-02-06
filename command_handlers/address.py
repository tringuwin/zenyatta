from helpers import make_string_from_word_list
from user import user_exists

async def address_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await message.channel.send("You are not registered yet. Please register first.")
        return

    user_address = make_string_from_word_list(message.content.split(), 1)
    
    users = db['users']
    users.update_one({'discord_id': message.author.id}, {'$set': {'address': user_address}})

    await message.channel.send('Your address has been added successfully!')