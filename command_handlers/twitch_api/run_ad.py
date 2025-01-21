

from command_handlers.twitch_api.twitch_helpers import get_broadcaster_id_from_channel, get_client_id, get_twitch_token
import requests

def run_ad_twitch_call(headers, data):

    result = requests.post('https://api.twitch.tv/helix/channels/commercial', headers=headers, json=data)
    print(result)
    result_json = result.json()
    print(result_json)


def make_run_ad_headers(db, channel_name):

    return {
        'Authorization': 'Bearer '+get_twitch_token(db, channel_name),
        'Client-Id': get_client_id(channel_name),
        'Content-Type': 'application/json'
    }

def make_run_ad_data(channel_name):

    return {
        'broadcaster_id': get_broadcaster_id_from_channel(channel_name),
        'length': 90
    }


async def run_ad(db, message, channel_name):

    headers = make_run_ad_headers(db, channel_name)
    data = make_run_ad_data(channel_name)

    result = run_ad_twitch_call(headers, data)