
from discord_actions import get_member_by_username
from user import twitch_user_exists, user_exists
import constants

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
        
    twitch_user = twitch_user_exists(db, user_id)
    if twitch_user:
        return twitch_user

    member = await get_member_by_username(client, user_id)
    user = None
    if member:
        user = user_exists(db, member.id)
    
    return user


def get_constant_value(db, constant_name):

    constants_db = db['constants']
    constant_obj = constants_db.find_one({'name': constant_name})
    if not constant_obj:
        return None
    
    return constant_obj['value']

def set_constant_value(db, constant_name, new_val):

    constants_db = db['constants']
    constants_db.update_one({"name": constant_name}, {"$set": {"value": new_val}})
    
def update_token_tracker(db, source, num):

    token_tracker = get_constant_value(db, 'token_tracker')

    if source in token_tracker:

        token_tracker[source]['total'] += num
        if num > 0:
            token_tracker[source]['given'] += num
        elif num < 0:
            token_tracker[source]['taken'] += abs(num)

    else:

        new_tracked_source = {
            'total': num,
            'given': 0,
            'taken': 0,
        }

        if num > 0:
            new_tracked_source['given'] += num
        elif num < 0:
            new_tracked_source['taken'] += abs(num)

        token_tracker[source] = new_tracked_source

    set_constant_value(db, 'token_tracker', token_tracker)


def get_league_emoji_from_team_name(team_name):

    if team_name in constants.TEAM_NAME_TO_EMOJI_EMBED_STRING:
        return constants.TEAM_NAME_TO_EMOJI_EMBED_STRING[team_name]
    
    return constants.DEFAULT_TEAM_EMOJI


def is_bot_commands_channel(channel):

    return (channel.id == constants.BOT_CHANNEL) or (channel.id == constants.RIVALS_BOT_CHANNEL) or (channel.id == constants.VALORANT_BOT_CHANNEL) or (channel.id == 1344702713086218432) # fake league commands channel


def is_valid_hex_code(s):
    # Optional: Check for starting hash symbol and adjust the string
    if s.startswith('#'):
        s = s[1:]

    # Check the length of the string
    if len(s) not in [3, 6]:
        return False

    # Check each character
    for char in s:
        if char.lower() not in "0123456789abcdef":
            return False

    return True