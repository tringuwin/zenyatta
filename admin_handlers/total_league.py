
async def total_league_handler(db, message):

    leagueteams = db['leagueteams']
    all_teams = leagueteams.find()

    total_players = 0
    total_teams = 0
    for team in all_teams:
        total_teams += 1
        total_players += len(team['members'])

    total_possible = int(total_teams * 25)

    await message.channel.send('Total players in SOL: '+str(total_players)+'/'+str(total_possible))