async def fix_mr_lineup_hander(db, message):
    rivals_league_teams = db['rivals_leagueteams']
    all_teams = rivals_league_teams.find()
    for team in all_teams:
        team['lineup'] = {
            'player1': {
                'role': 'player',
                'user_id': 0
            },
            'player2': {
                'role': 'player',
                'user_id': 0
            },
            'player3': {
                'role': 'player',
                'user_id': 0
            },
            'player4': {
                'role': 'player',
                'user_id': 0
            },
            'player5': {
                'role': 'player',
                'user_id': 0
            },
            'player6': {
                'role': 'player',
                'user_id': 0
            },
        }

        rivals_league_teams.update_one({'team_name': team['team_name']}, {'$set': {'lineup': team['lineup']}})
        
    await message.channel.send('All teams have been reset to have no players in their lineup.')