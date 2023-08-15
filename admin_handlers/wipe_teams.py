
async def wipe_teams_handler(db, message):
    
    teams = db['teams']
    teams.delete_many({})
    await message.channel.send('All teams have been deleted.')