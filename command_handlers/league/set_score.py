

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
from safe_send import safe_send


async def set_score_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    score_index = params[1]
    if not can_be_int(score_index):
        await safe_send(message.channel, score_index+' is not an integer')
        return
    
    score_index = int(score_index)
    if score_index > 4 or score_index < 1:
        await safe_send(message.channel, 'score index must be between 1 and 4')
        return
    
    score = params[2]
    if not can_be_int(score):
        await safe_send(message.channel, score+' is not an integer')
        return
    
    score = int(score)
    local_files = db['localfiles']
    files = local_files.find_one({'files_id': 1})

    files['files']['scores']['data']['score'+str(score_index)] = score
    files['files']['scores']['version'] += 1

    local_files.update_one({"files_id": 1}, {"$set": {"files": files['files']}})

    await safe_send(message.channel, 'Score updated')