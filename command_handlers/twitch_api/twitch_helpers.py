
import constants
from helpers import get_constant_value


VALID_TWITCH_CHANNELS = ['main', 'second', 'third']

def get_twitch_token(db, channel_name):

    if channel_name == 'main':
        return get_constant_value(db, 'twitch_token')
    elif channel_name == 'second':
        return get_constant_value(db, 'twitch_token_second')
    elif channel_name == 'third':
        return get_constant_value(db, 'twitch_token_third')
    
    raise Exception('Could not find token for channel name: '+channel_name)


def is_valid_channel(channel_name):

    valid_channel = channel_name in VALID_TWITCH_CHANNELS
    return valid_channel



CHANNEL_NAME_TO_CLIENT_ID = {
    'main': constants.TWITCH_CLIENT_ID,
    'second': constants.SECOND_CLIENT_ID,
    'third': constants.THIRD_CLIENT_ID
}

def get_client_id(channel_name):

    return CHANNEL_NAME_TO_CLIENT_ID[channel_name]



def get_callback_url(channel_name):

    if channel_name == 'main':
        return 'https://spicy-ragu-api-7d24f98c9e91.herokuapp.com/dva-webhook'
    elif channel_name == 'second':
        return 'https://spicy-ragu-api-7d24f98c9e91.herokuapp.com/dva-webhook-2'
    elif channel_name == 'third':
        return 'https://spicy-ragu-api-7d24f98c9e91.herokuapp.com/dva-webhook-3'
    
    raise Exception('Could not find callback url for channel name: '+channel_name)


def get_broadcaster_id_from_channel(channel):

    if channel == 'main':
        return constants.MAIN_BROADCASTER_ID
    elif channel == 'second':
        return constants.SECOND_BROADCASTER_ID
    elif channel == 'third':
        return constants.THIRD_BROADCASTER_ID
    
    raise Exception('Invalid channel name in get broadcaster id')


def get_twitch_constant_name_from_channel(channel):

    if channel == 'main':
        return 'twitch_main_pred'
    elif channel == 'second':
        return 'twitch_second_pred'
    elif channel == 'third':
        return 'twitch_third_pred'
    
    raise Exception('Invalid channel name in get twitch constant.')