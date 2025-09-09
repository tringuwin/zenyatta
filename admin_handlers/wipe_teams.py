
from safe_send import safe_send


async def wipe_teams_handler(db, message):
    
    teams = db['teams']
    teams.delete_many({})
    
    await safe_send(message.channel, 'All teams have been deleted.')