

from command_handlers.twitch_api.twitch_helpers import get_broadcaster_id_from_channel, get_client_id, get_twitch_constant_name_from_channel, get_twitch_token, is_valid_channel
from common_messages import invalid_number_of_params
from helpers import get_constant_value, valid_number_of_params
import requests

def make_end_pred_headers(db, channel):

    return {
        'Authorization': 'Bearer '+get_twitch_token(db, channel),
        'Client-Id': get_client_id(channel)
    }


def end_pred_twitch_call(db, channel, prediction_id, winning_id):

    headers = make_end_pred_headers(db, channel)

    broadcaster_id = get_broadcaster_id_from_channel(channel)

    prediction_params = '?broadcaster_id='+broadcaster_id+'&id='+str(prediction_id)+'&status=resolved&winning_outcome_id='+winning_id

    response = requests.patch('https://api.twitch.tv/helix/predictions'+prediction_params, headers=headers)
    status_code = response.status_code

    if status_code == 200:
        return True
    
    return False



async def end_pred(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    channel = params[1]
    channel_lower = channel.lower()
    choice = params[2]
    choice_lower = choice.lower()

    if not is_valid_channel(channel_lower):
        await message.channel.send(channel+' is not a valid channel name. It must be either main, second or third.')
        return

    constant_name = get_twitch_constant_name_from_channel(channel_lower)
    pred_data = get_constant_value(db, constant_name)

    pred_choice = -1
    if choice_lower == pred_data['outcomes'][0]['title'].lower():
        pred_choice = 0
    elif choice_lower == pred_data['outcomes'][1]['title'].lower():
        pred_choice = 1

    if pred_choice == -1:
        await message.channel.send('Could not find a prediction result with the name '+choice)

    worked = end_pred_twitch_call(db, channel_lower, pred_data['pred_id'], pred_data['outcomes'][pred_choice]['outcome_id'])
    if not worked:
        await message.channel.send('Something went wrong.')
        return
    
    await message.channel.send('Prediction ended.')
    