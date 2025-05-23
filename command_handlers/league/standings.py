
import constants
from context.context_helpers import get_league_url_from_context
from helpers import get_constant_value, get_league_emoji_from_team_name


def make_div_standings_string(div_teams, div_num):

    div_string = '**DIVISION '+str(div_num)+' STANDINGS:**'

    index = 1 
    for team in div_teams:
        team_emoji_string = get_league_emoji_from_team_name(team['team_name'])
        rank_emoji = '⬜'
        if index == 1:
            rank_emoji = '🟩'
        elif index == 2 or index == 3:
            rank_emoji = '🟦'
        # elif index == 5 and div_num != 4:
        #     rank_emoji = '🟥'
        div_string += '\n'+rank_emoji+' '+str(index)+'. '+team_emoji_string+' '+team['team_name']+' | '+str(team['team'][0])+' W | '+str(team['team'][1])+' L | '+str(team['win_percent'])+'% | MD: '+str(team['team'][2]) 
        index += 1

    return div_string

async def standings_handler_old(db, message, client):

    league_season = get_constant_value(db, 'league_season')

    standings = db['standings']
    season_object = standings.find_one({'season': league_season})

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
                'score': score,
                'map_diff': team[2]
            }
        )

    div_groups = [[], [], [], []]
    for team in final_teams:
        if team['team_name'] in season_object['divs'][0]:
            div_groups[0].append(team)
        elif team['team_name'] in season_object['divs'][1]:
            div_groups[1].append(team)
        elif team['team_name'] in season_object['divs'][2]:
            div_groups[2].append(team)
        elif team['team_name'] in season_object['divs'][3]:
            div_groups[3].append(team)

    sorted_teams_1 = sorted(div_groups[0], key=lambda x: (x["score"], x["map_diff"]), reverse=True)
    sorted_teams_2 = sorted(div_groups[1], key=lambda x: (x["score"], x["map_diff"]), reverse=True)
    sorted_teams_3 = sorted(div_groups[2], key=lambda x: (x["score"], x["map_diff"]), reverse=True)
    sorted_teams_4 = sorted(div_groups[3], key=lambda x: (x["score"], x["map_diff"]), reverse=True)
    # start temp code
    stored = sorted_teams_2[0]
    sorted_teams_2[0] = sorted_teams_2[1]
    sorted_teams_2[1] = stored
    # end temp code
    final_string = '**LEAGUE STANDINGS**\n-----------------------'

    final_string += '\n'+make_div_standings_string(sorted_teams_1, 1)
    final_string += '\n-----------------------'
    final_string += '\n'+make_div_standings_string(sorted_teams_2, 2)
    final_string += '\n-----------------------'
    final_string += '\n'+make_div_standings_string(sorted_teams_3, 3)
    final_string += '\n-----------------------'
    final_string += '\n'+make_div_standings_string(sorted_teams_4, 4)

    final_string += '\n-----------------------'
    final_string += '\nTeams ranked 1-3 will make it to the playoffs.'
    final_string += '\n🟩 = Will play in Div Finals | 🟦 = Will play in Div Semi-Finals | ⬜ = Will miss playoffs'#| 🟥 = Will be relegated to lower Div next season'
    #final_string += '\nTeam ranked 7-10th will be demoted to Division 2 next season.'

    await message.channel.send(final_string)
    


async def standings_main(db, message, client, top):

    league_season = get_constant_value(db, 'league_season')

    standings = db['standings']
    season_object = standings.find_one({'season': league_season})

    all_teams = []
    for team_name in season_object['teams']:
        team_obj = season_object['teams'][team_name]
        team_obj['team_name'] = team_name
        all_teams.append(team_obj)

    sorted_teams = sorted(all_teams, key=lambda x: (x["points"], x["wins"], x['map_wins']), reverse=True)

    teams_to_log = []
    if top:
        for i in range(12):
            teams_to_log.append(sorted_teams[i])
    else:
        for i in range(12, 24):
            teams_to_log.append(sorted_teams[i])

    final_string = '**SEASON '+str(league_season)+' STANDINGS (TOP 12)**\n' if top else '**SEASON '+str(league_season)+' STANDINGS (BOTTOM 12)**\n'
    detail_string = 'To view the bottom 12 teams, use the command **!standings2**' if top else 'To view the top 12 teams, use the command **!standings**'

    rank = 1 if top else 13

    for team in teams_to_log:

        team_emoji_string = get_league_emoji_from_team_name(team['team_name'])

        map_string = str(team['map_wins'])+' MW | '+str(team['map_losses'])+' ML | '

        final_string += '\n'+str(rank)+'. '+team_emoji_string+' '+team['team_name']+' | '+str(team['points'])+' PTS | '+str(team['wins'])+' W | '+str(team['losses'])+' L | '+map_string

        rank += 1

    final_string += '\n\n'+detail_string

    await message.channel.send(final_string)

        
async def standings_handler(message, context):

    league_url = get_league_url_from_context(context)

    await message.reply(f'Check out the standings for the league here!\n\nhttps://spicyesports.com/{league_url}/standings')

    # await standings_main(db, message, client, True)


async def standings2_handler(db, message, client):

    await standings_main(db, message, client, False)