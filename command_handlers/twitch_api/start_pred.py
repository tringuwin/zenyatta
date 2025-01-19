
import requests
from helpers import can_be_int, get_constant_value, set_constant_value, valid_number_of_params
import constants


def get_twitch_token(db):

    return get_constant_value(db, 'twitch_token')



def make_start_pred_headers(db):

    return {
        'Authorization': 'Bearer '+get_twitch_token(db),
        'Client-Id': constants.TWITCH_CLIENT_ID,
        'Content-Type': 'application/json'
    }



def start_pred_twitch_call(db, data):

    headers = make_start_pred_headers(db)

    response = requests.post('https://api.twitch.tv/helix/predictions', headers=headers, json=data)
    response_json = response.json()

    return response_json


async def start_pred(db, message):

    valid_params, params = valid_number_of_params(message, 4)
    if not valid_params:
        await message.reply('The command was not formatted correctly. There can only be two options and each option must be one word. The last part is how many minutes it will be open. Example: **!startpred Polar Olympians 10**')
        return

    choice1 = params[1]
    choice2 = params[2]
    minutes = params[3]

    if not can_be_int(minutes):
        await message.channel.send(minutes+' is not a number.')
        return
    minutes = int(minutes)
    seconds = minutes * 60

    data = {
        'broadcaster_id': constants.MAIN_BROADCASTER_ID,
        'prediction_window': seconds,
        'title': 'Who will win?',
        'outcomes': [{'title': choice1}, {'title': choice2}]
    }

    twitch_json = start_pred_twitch_call(db, data)
    if twitch_json:
        twitch_data = twitch_json['data'][0]
        prediction_id = twitch_data['id']
        outcomes = twitch_json['outcomes']
        
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

        set_constant_value(db, 'twitch_main_pred', save_object)

    await message.channel.send('Successfully saved prediction.')








