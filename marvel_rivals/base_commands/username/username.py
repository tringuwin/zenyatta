

from helpers import make_string_from_word_list
from marvel_rivals.base_commands.username.utils.create_new_user import create_new_user
from marvel_rivals.base_commands.username.utils.update_user_username import update_user_username
from user import user_exists

async def username_handler(db, message):

    word_parts = message.content.split()
    rivals_username = make_string_from_word_list(word_parts, 1)
    print('submitted username '+str(rivals_username))

    if len(rivals_username) > 30:
        await message.channel.send('The marvel rivals username you provided is not valid.')
        return


    user_id = message.author.id
    user = user_exists(db, user_id)
    if user_exists(db, user_id):
        update_user_username(db, user, message) 
    else:
        create_new_user(db, user_id, message)

    await message.channel.send('Hit username handler')