

from automation.schedule_plan.notif_helpers.notify_staff_for_matches import notify_staff_for_matches


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


def get_teams_without_matches(team_has_match_dict):

    teams_without_matches = []
    for team in team_has_match_dict:
        if not team_has_match_dict[team]:
            teams_without_matches.append(team)

    return teams_without_matches

async def check_if_matches_are_set(db, schedule_plans, schedule, week, message, current_week):

    league_context = schedule['context']
    season = schedule['season']
    actual_week = current_week + 1

    team_has_match_dict = make_team_has_match_dict(schedule['season_teams'])
    all_matchups = get_all_matchups(db, league_context, season, actual_week)

    for matchup in all_matchups:

        if (not matchup['team1'] in team_has_match_dict):
            await message.channel.send(f'Team {matchup["team1"]} is not in the league')
            return
        
        if (not matchup['team2'] in team_has_match_dict):
            await message.channel.send(f'Team {matchup["team2"]} is not in the league')
            return
        
        team_has_match_dict[matchup['team1']] = True
        team_has_match_dict[matchup['team2']] = True

    teams_without_matches = get_teams_without_matches(team_has_match_dict)

    if len(teams_without_matches) == 0:
        pass
    else:

        await message.channel.send(f'Teams without matches: {teams_without_matches}')
        await notify_staff_for_matches(message, schedule)