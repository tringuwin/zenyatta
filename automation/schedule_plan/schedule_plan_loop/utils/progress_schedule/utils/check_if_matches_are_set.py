

def get_all_matchups(db, league_context, season, week):

    matchups_collection = db['matchups']

    matchups = matchups_collection.find({
        'context': league_context,
        'season': season,
        'week': week
    })

    return matchups


def make_team_has_match_dict(teams):

    team_has_match_dict = {}
    for team in teams:
        team_has_match_dict[team['team_name']] = False

    return team_has_match_dict


async def check_if_matches_are_set(db, schedule_plans, schedule, week, message, current_week):

    league_context = schedule['context']
    season = schedule['season']
    actual_week = current_week + 1

    team_has_match_dict = make_team_has_match_dict(schedule['season_teams'])
    all_matchups = get_all_matchups(db, league_context, season, actual_week)

    # for matchup in all_matchups:

    #     if (not matchup['tea'])