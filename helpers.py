
from discord_actions import get_member_by_username
from user import twitch_user_exists, user_exists


def valid_number_of_params(message, num_params):
    
    message_parts = message.content.split(' ')
    valid = len(message_parts) == num_params

    return valid, message_parts

def valid_params_ignore_whitespace(message, num_params):

    message_parts = message.content.split()
    valid = len(message_parts) == num_params

    return valid, message_parts

def can_be_int(var):
    try:
        int(var)
        return True
    except ValueError:
        return False

def make_string_from_word_list(word_list, start_index):

    info = ''

    section_index = start_index
    while section_index < len(word_list):
        info += word_list[section_index]
        section_index += 1
        if section_index != len(word_list):
            info += ' '

    return info


async def generic_find_user(client, db, user_id):

    if can_be_int(user_id):
        user = user_exists(db, int(user_id))
        if user:
            return user
        
    twitch_user = twitch_user_exists(user_id)
    if twitch_user:
        return twitch_user

    member = await get_member_by_username(client, user_id)
    user = None
    if member:
        user = user_exists(db, member.id)
    
    return user
