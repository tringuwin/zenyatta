
import constants
from context.context_helpers import get_league_teams_collection_from_context, get_team_owners_channel_from_context


def make_week_match_days(all_matchups):

    match_days = {
        'Wednesday': [],
        'Thursday': [],
        'Friday': [],
        'Saturday': [],
        'Sunday': []
    }

    for matchup in all_matchups:
        match_timeslot = matchup['timeslot']
        timeslot_info = constants.TIMESLOT_TO_INFO[match_timeslot]
        match_day = timeslot_info[0]
        match_time_est = timeslot_info[1]
        match_days[match_day].append([match_time_est, matchup])

    return {
        'Wednesday': sorted(match_days['Wednesday'], key=lambda x: x[0]),
        'Thursday': sorted(match_days['Thursday'], key=lambda x: x[0]),
        'Friday': sorted(match_days['Friday'], key=lambda x: x[0]),
        'Saturday': sorted(match_days['Saturday'], key=lambda x: x[0]),
        'Sunday': sorted(match_days['Sunday'], key=lambda x: x[0])
    }


async def notify_team_owners_of_schedule(client, db, schedule, all_matchups):

    actual_week = schedule['current_week'] + 1
    context = schedule['context']
    
    team_owners_channel = get_team_owners_channel_from_context(client, context)
    league_teams = get_league_teams_collection_from_context(db, context)

    matchups_message = f'**FINAL SCHEDULE FOR WEEK {actual_week}**'
    all_team_pings = ''

    week_match_days = make_week_match_days(all_matchups)
    for match_day_name in week_match_days:
        match_day_matchups = week_match_days[match_day_name]
        if len(match_day_matchups) == 0:
            continue

        matchups_message += f'\n\n**{match_day_name}**'
        for match_time, matchup in match_day_matchups:
            matchups_message += f'\n{match_time}:00 PM EST - {matchup["team1"]} VS {matchup["team2"]}'

            team1 = league_teams.find_one({'team_name': matchup['team1']})
            team2 = league_teams.find_one({'team_name': matchup['team2']})

            team_1_ping = '<@&'+str(team1['team_role_id'])+'>'
            team_2_ping = '<@&'+str(team2['team_role_id'])+'>'

            all_team_pings += f'{team_1_ping} {team_2_ping} '

    matchups_message += '\n\n'+all_team_pings
    await team_owners_channel.send(matchups_message)

