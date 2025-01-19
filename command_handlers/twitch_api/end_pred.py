

from command_handlers.twitch_api.twitch_helpers import get_twitch_token
from common_messages import invalid_number_of_params
from helpers import get_constant_value, valid_number_of_params
import constants
import requests

def make_end_pred_headers(db):

    return {
        'Authorization': 'Bearer '+get_twitch_token(db),
        'Client-Id': constants.TWITCH_CLIENT_ID
    }


def end_pred_twitch_call(db, prediction_id, winning_id):

    headers = make_end_pred_headers(db)

    prediction_params = '?broadcaster_id='+constants.MAIN_BROADCASTER_ID+'&id='+str(prediction_id)+'&status=resolved&winning_outcome_id='+winning_id

    response = requests.patch('https://api.twitch.tv/helix/predictions'+prediction_params, headers=headers)
    status_code = response.status_code

    if status_code == 200:
        return True
    
    return False



async def end_pred(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    choice = params[1]
    choice_lower = choice.lower()

    pred_data = get_constant_value(db, 'twitch_main_pred')

    pred_choice = -1
    if choice_lower == pred_data['outcomes'][0]['title'].lower():
        pred_choice = 0
    elif choice_lower == pred_data['outcomes'][1]['title'].lower():
        pred_choice = 1

    if pred_choice == -1:
        await message.channel.send('Could not find a prediction result with the name '+choice)

    worked = end_pred_twitch_call(db, pred_data['pred_id'], pred_data['outcomes'][pred_choice]['outcome_id'])
    if not worked:
        await message.channel.send('Something went wrong.')
        return
    
    await message.channel.send('Prediction ended.')
    