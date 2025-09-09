
from safe_send import safe_send


async def reset_scores_handler(db, message):

    local_files = db['localfiles']
    files = local_files.find_one({'files_id': 1})

    for x in range(4):
        files['files']['scores']['data']['score'+str(x+1)] = 0
    
    files['files']['scores']['version'] += 1

    local_files.update_one({"files_id": 1}, {"$set": {"files": files['files']}})

    await safe_send(message.channel, 'scores reset')