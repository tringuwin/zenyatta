
async def total_league_handler(db, message):

    leagueteams = db['leagueteams']
    all_teams = leagueteams.find()

    total_players = 0
    for team in all_teams:
        total_players += len(team['members'])

    await message.channel.send('Total players in SOL: '+str(total_players))