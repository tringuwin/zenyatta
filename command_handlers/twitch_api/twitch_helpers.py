
import constants
from helpers import get_constant_value




def get_twitch_token(db):

    return get_constant_value(db, 'twitch_token')


def is_valid_channel(channel_name):

    return ((channel_name == 'main') or (channel_name == 'second'))


def get_broadcaster_id_from_channel(channel):

    if channel == 'main':
        return constants.MAIN_BROADCASTER_ID
    elif channel == 'second':
        return constants.SECOND_BROADCASTER_ID
    
    raise Exception('Invalid channel name in get broadcaster id')


def get_twitch_constant_name_from_channel(channel):

    if channel == 'main':
        return 'twitch_main_pred'
    elif channel == 'second':
        return 'twitch_second_pred'
    
    raise Exception('Invalid channel name in get twitch constant.')