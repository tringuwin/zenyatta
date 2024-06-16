

from discord_actions import get_guild
import constants


def make_div_standings_string(div_teams, div_num, guild):

    div_string = '**DIVISION '+str(div_num)+' STANDINGS:**'

    index = 1 
    for team in div_teams:
        team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team['team_name']]
        team_emoji = guild.get_emoji(team_emoji_id)
        rank_emoji = '⬜'
        if index == 0:
            rank_emoji = '🟩'
        elif index == 4:
            rank_emoji = '🟥'
        div_string += '\n'+rank_emoji+str(index)+'. '+str(team_emoji)+' '+team['team_name']+' | '+str(team['team'][0])+' W | '+str(team['team'][1])+' L | '+str(team['win_percent'])+'%'
        index += 1

    return div_string

async def standings_handler(db, message, client):

    standings = db['standings']
    season_object = standings.find_one({'season': constants.LEAGUE_SEASON})

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

    div_groups = [[], [], []]
    for team in final_teams:
        if team['team_name'] in season_object['divs'][0]:
            div_groups[0].append(team)
        elif team['team_name'] in season_object['divs'][1]:
            div_groups[1].append(team)
        elif team['team_name'] in season_object['divs'][2]:
            div_groups[2].append(team)

    sorted_teams_1 = sorted(div_groups[0], key=lambda x: x["score"], reverse=True)
    sorted_teams_2 = sorted(div_groups[1], key=lambda x: x["score"], reverse=True)
    sorted_teams_3 = sorted(div_groups[2], key=lambda x: x["score"], reverse=True)
    final_string = '**LEAGUE STANDINGS**\n-----------------------'
    guild = await get_guild(client)

    final_string += '\n'+make_div_standings_string(sorted_teams_1, 1, guild)
    final_string += '\n-----------------------'
    final_string += '\n'+make_div_standings_string(sorted_teams_2, 2, guild)
    final_string += '\n-----------------------'
    final_string += '\n'+make_div_standings_string(sorted_teams_3, 3, guild)

    final_string += '\n-----------------------'
    final_string += '\nTeams ranked 1-3 will make it to the playoffs.'
    #final_string += '\nTeam ranked 7-10th will be demoted to Division 2 next season.'
    #final_string += '\nSee the standings page on the website here: https://spicyragu.netlify.app/sol/standings'

    await message.channel.send(final_string)
    

        