

from command_handlers.twitch_api.twitch_helpers import get_broadcaster_id_from_channel, get_client_id, get_twitch_token
import requests

def run_ad_twitch_call(headers, data):

    result = requests.post('https://api.twitch.tv/helix/channels/commercial', headers=headers, json=data)
    return result


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

async def respond_based_on_result(message, result):

    status_code = result.status_code

    if status_code == 200:
        await message.channel.send('Ad started successfully.')
        return

    elif status_code == 400:
        await message.channel.send('This channel is not currently live, so ads cannot be run.')
        return
    
    await message.channel.send('Something went wrong...')


async def run_ad(db, message, channel_name):

    headers = make_run_ad_headers(db, channel_name)
    data = make_run_ad_data(channel_name)

    result = run_ad_twitch_call(headers, data)
    await respond_based_on_result(message, result)