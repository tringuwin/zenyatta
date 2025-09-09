

from safe_send import safe_send


async def reset_wins_handler(db, message):

    local_files = db['localfiles']
    files = local_files.find_one({'files_id': 1})

    for x in range(7):
        files['files']['map_wins']['data']['map'+str(x+1)] = 'None'
    
    files['files']['map_wins']['version'] += 1

    local_files.update_one({"files_id": 1}, {"$set": {"files": files['files']}})

    await safe_send(message.channel, 'wins reset')