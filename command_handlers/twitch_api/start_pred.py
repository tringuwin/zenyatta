
import requests
from command_handlers.twitch_api.twitch_helpers import get_broadcaster_id_from_channel, get_client_id, get_twitch_constant_name_from_channel, get_twitch_token, is_valid_channel
from helpers import can_be_int, set_constant_value, valid_number_of_params
import constants




def make_start_pred_headers(db, channel_name):

    return {
        'Authorization': 'Bearer '+get_twitch_token(db, channel_name),
        'Client-Id': get_client_id(channel_name),
        'Content-Type': 'application/json'
    }



def start_pred_twitch_call(db, data, channel_name):

    headers = make_start_pred_headers(db, channel_name)

    response = requests.post('https://api.twitch.tv/helix/predictions', headers=headers, json=data)
    response_json = response.json()
    print(response_json)

    return response_json


async def start_pred(db, message):

    valid_params, params = valid_number_of_params(message, 5)
    if not valid_params:
        await message.reply('The command was not formatted correctly. There can only be two options and each option must be one word. The last part is how many minutes it will be open. Example: **!startpred main Polar Olympians 10**')
        return

    channel = params[1]
    channel_lower = channel.lower()
    choice1 = params[2]
    choice2 = params[3]
    minutes = params[4]

    if not is_valid_channel(channel_lower):
        await message.channel.send(channel+' is not a valid channel name. It must be either main or second.')
        return

    if not can_be_int(minutes):
        await message.channel.send(minutes+' is not a number.')
        return
    minutes = int(minutes)
    seconds = minutes * 60

    data = {
        'broadcaster_id': get_broadcaster_id_from_channel(channel_lower),
        'prediction_window': seconds,
        'title': 'Who will win?',
        'outcomes': [{'title': choice1}, {'title': choice2}]
    }

    twitch_json = start_pred_twitch_call(db, data, channel_lower)
    if twitch_json:
        print(twitch_json)
        twitch_data = twitch_json['data'][0]
        prediction_id = twitch_data['id']
        outcomes = twitch_data['outcomes']
        
        save_object = {
            'pred_id': prediction_id,
            'outcomes': [
                {
                    'title': outcomes[0]['title'],
                    'outcome_id': outcomes[0]['id']
                },
                {
                    'title': outcomes[1]['title'],
                    'outcome_id': outcomes[1]['id']
                }
            ]
        }

        constant_name = get_twitch_constant_name_from_channel(channel_lower)
        set_constant_value(db, constant_name, save_object)

    await message.channel.send('Started prediction.')








