

from discord_actions import get_guild
from helpers import pad_string_to_length
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
        win_percent = 0
        if total_matches != 0:
            win_percent = float(team[0]) / float(total_matches)
            win_percent = str(round(win_percent, 2))

        final_teams.append(
            {
                'team': team,
                'win_percent': win_percent,
                'team_name': team_name
            }
        )
        

    sorted_teams = sorted(final_teams, key=lambda x: x["win_percent"], reverse=True)
    final_string = '**LEAGUE STANDINGS**\n-----------------------'
    index = 1 
    guild = await get_guild(client)
    for team in sorted_teams:
        team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team['team_name']]
        team_emoji = guild.get_emoji(team_emoji_id)
        final_string += '\n'+str(index)+'. '+str(team_emoji)+' '+team['team_name']+' | '+str(team['team'][0])+' W | '+str(team['team'][1])+' L | '+str(team['win_percent'])+'%'
        index += 1

    await message.channel.send(final_string)
    

        