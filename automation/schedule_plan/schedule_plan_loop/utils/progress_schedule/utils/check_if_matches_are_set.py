

from automation.schedule_plan.notif_helpers.notify_staff_for_matches import notify_staff_for_matches
from automation.schedule_plan.notif_helpers.notify_team_owners_of_matches import notify_team_owners_of_matches
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_if_should_generate_matchups import check_if_should_generate_matchups
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.get_all_matchups import get_all_matchups
from safe_send import safe_send



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

async def check_if_matches_are_set(client, db, schedule_plans, schedule, message, current_week):

    league_context = schedule['context']
    season = schedule['season']
    actual_week = current_week + 1

    team_has_match_dict = make_team_has_match_dict(schedule['season_teams'])
    all_matchups = get_all_matchups(db, league_context, season, actual_week)

    if len(all_matchups) == 0:
        await check_if_should_generate_matchups(message, db, schedule)
        return

    for matchup in all_matchups:

        if (not matchup['team1'] in team_has_match_dict):
            await safe_send(message.channel, f'Team {matchup["team1"]} is not in the league')
            return
        
        if (not matchup['team2'] in team_has_match_dict):
            await safe_send(message.channel, f'Team {matchup["team2"]} is not in the league')
            return
        
        team_has_match_dict[matchup['team1']] = True
        team_has_match_dict[matchup['team2']] = True

    teams_without_matches = get_teams_without_matches(team_has_match_dict)

    if len(teams_without_matches) == 0:
        await notify_team_owners_of_matches(client, db, all_matchups, league_context, actual_week)

        schedule['weeks'][current_week]['status'] = 'SCHEDULING'
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})
        await safe_send(message.channel, f'Matches are set for week {actual_week} of season {season} of league {league_context} and team owners have been notified.')

    else:
        await safe_send(message.channel, f'Teams without matches: {teams_without_matches}')
        await notify_staff_for_matches(message, schedule)