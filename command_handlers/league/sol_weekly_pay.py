
from helpers import get_constant_value


TOKENS_PER_TIER = {

    1: 5000,
    2: 4000,
    3: 3500,
    4: 3000,

    5: 2800,
    6: 2600,
    7: 2400,
    8: 2200,

    9: 2000,
    10: 1900,
    11: 1800,
    12: 1700,

    13: 1600,
    14: 1500,
    15: 1400,
    16: 1300,

    17: 1200,
    18: 1100,
    19: 1000,
    20: 900,

    21: 800,
    22: 700,
    23: 600,
    24: 500,

}

def sort_league_teams_by_points(all_teams):

    return sorted(all_teams, key=lambda x: (x["score"]), reverse=True) 


def group_teams_by_score(sorted_teams):

    groups_of_teams_by_score = {}

    place_index = 1
    for i in range(len(sorted_teams)):

        team = sorted_teams[i]
        team_score = team['score']

        score_group = groups_of_teams_by_score[team_score]
        if score_group:
            score_group['teams'].append(team)
            score_group['lowest_place'] = place_index
        else:
            groups_of_teams_by_score[team_score] = {
                'lowest_place': place_index,
                'teams': [team]
            }

        place_index += 1

    print(groups_of_teams_by_score)




async def sol_weekly_pay(db, message):

    league_season = get_constant_value(db, 'league_season')

    standings_db = db['standings']
    season_standings = standings_db.find_one({'season': league_season})
    if not season_standings:
        await message.channel.send('Could not find the standings for season '+str(league_season))
        return
    
    all_teams = season_standings['teams']
    array_of_teams = []
    for team_name in all_teams:
        team_obj = all_teams[team_name]
        team_obj['name'] = team_name
        array_of_teams.append(team_obj)

    sorted_teams = sort_league_teams_by_points(all_teams)

    groups_of_teams_by_score = group_teams_by_score(sorted_teams)

    
