

from discord_actions import get_guild
import constants


season = 1

async def standings_handler(db, message, client):

    standings = db['standings']
    season_object = standings.find_one({'season': season})

    final_teams = []
    teams = season_object['teams']
    for team_name in teams:
        team = teams[team_name]
        total_matches = team[0] + team[1]
        win_percent = 0.0
        score = 0
        if total_matches != 0:
            win_percent = float(team[0]) / float(total_matches)
            win_percent = round(win_percent*100, 2)
            score = team[0] - team[1]

        final_teams.append(
            {
                'team': team,
                'win_percent': win_percent,
                'team_name': team_name,
                'score': score
            }
        )
        

    sorted_teams = sorted(final_teams, key=lambda x: x["score"], reverse=True)
    final_string = '**LEAGUE STANDINGS**\n-----------------------'
    index = 1 
    guild = await get_guild(client)
    for team in sorted_teams:
        team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team['team_name']]
        team_emoji = guild.get_emoji(team_emoji_id)
        final_string += '\n'+str(index)+'. '+str(team_emoji)+' '+team['team_name']+' | '+str(team['team'][0])+' W | '+str(team['team'][1])+' L | '+str(team['win_percent'])+'%'
        index += 1

    final_string += '\n-----------------------'
    final_string += '\nTeams ranked 1-3 will make it to the playoffs.'
    final_string += '\nTeam ranked 5th will be demoted to division 2 next season.'

    await message.channel.send(final_string)
    

        