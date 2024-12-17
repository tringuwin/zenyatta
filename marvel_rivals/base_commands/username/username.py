

from helpers import make_string_from_word_list
from marvel_rivals.base_commands.username.utils.create_new_user import create_new_user
from marvel_rivals.base_commands.username.utils.update_user_username import update_user_username
from user import user_exists

def user_with_username_exists(db, username):

    username_lower = username.lower()

    users = db['users']
    username_user = users.find_one({'rivals_username_lower': username_lower})

    if username_user:
        return True
    
    return False


async def username_handler(db, message):

    word_parts = message.content.split()
    rivals_username = make_string_from_word_list(word_parts, 1)
    print('submitted username "'+str(rivals_username)+'"')

    if len(rivals_username) > 30 or len(rivals_username) < 1:
        await message.channel.send('The marvel rivals username you provided is not valid.')
        return
    
    if user_with_username_exists(db, rivals_username):
        await message.channel.send('That marvel rivals username is already linked to a user. (Maybe you already linked it?)')
        return

    user_id = message.author.id
    user = user_exists(db, user_id)
    if user_exists(db, user_id):
        await update_user_username(db, user, message, rivals_username) 
    else:
        await create_new_user(db, user_id, message, rivals_username)
