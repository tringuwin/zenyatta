

from safe_send import safe_send


async def weekly_roster_reset(db, message):

    league_teams = db['leagueteams']
    all_teams = league_teams.find()

    for team in all_teams:
        team_lineup = team['lineup']

        for role_name in team_lineup:
            team_lineup[role_name]['user_id'] = 0
            league_teams.update_one({'team_name': team['team_name']}, {'$set': {'lineup': team_lineup}})

    await safe_send(message.channel, 'Reset lineups for all league teams')
