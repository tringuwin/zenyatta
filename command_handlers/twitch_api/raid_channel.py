

import requests
from command_handlers.twitch_api.twitch_helpers import get_broadcaster_id_from_channel, get_client_id, get_twitch_token


def raid_twitch_call(headers, from_id, to_id):

    result = requests.post(f'https://api.twitch.tv/helix/raids?from_broadcaster_id={from_id}&to_broadcaster_id={to_id}', headers=headers)
    return result


def make_raid_headers(db, channel_name):

    return {
        'Authorization': 'Bearer '+get_twitch_token(db, channel_name),
        'Client-Id': get_client_id(channel_name),
    }



async def respond_based_on_result(message, result):

    status_code = result.status_code

    if status_code == 200:
        await message.channel.send('Raid started successfully.')
        return

    elif status_code == 400:
        await message.channel.send('Raid could not be started.')
        return
    
    print(result)
    print(result.json())
    await message.channel.send('Something went wrong...')


async def raid_channel(db, message, from_channel, to_channel):

    headers = make_raid_headers(db, from_channel)
    from_channel_id = get_broadcaster_id_from_channel(from_channel)
    to_channel_id = get_broadcaster_id_from_channel(to_channel)

    result = raid_twitch_call(headers, from_channel_id, to_channel_id)
    await respond_based_on_result(message, result)