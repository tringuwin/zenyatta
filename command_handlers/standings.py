

from helpers import pad_string_to_length


season = 1

async def standings_handler(db, message):

    standings = db['standings']
    season_object = standings.find_one({'season': season})

    teams = season_object['teams']
    for team_name in teams:
        team = teams['team_name']
        total_matches = team[0] + team[1]
        win_percent = 0
        if total_matches != 0:
            win_percent = float(team[0]) / float(total_matches)
            win_percent = str(round(win_percent, 2))

        team['win_percent'] = win_percent

    sorted_teams = sorted(teams, key=lambda x: x["win_percent"], reverse=True)
    final_string = '**LEAGUE STANDINGS**\n-----------------------'
    for team_name in sorted_teams:
        final_string += '\n'+pad_string_to_length(team_name, 20)+'|'

    await message.channel.send(final_string)
    

        