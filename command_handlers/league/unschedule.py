
import constants
from command_handlers.league.timeslot import get_team_index, get_team_matchup
from context.context_helpers import get_league_teams_collection_from_context, get_team_owners_channel_from_context
from league import validate_admin
from safe_send import safe_send

TIMESLOT_PREFIX_TO_DAY_INDEX = {
    'W': 2,
    'T': 3,
    'F': 4,
    'S': 5,
    'X': 6
}

def get_day_index_from_timeslot(timeslot):

    timeslot_day_prefix = timeslot.split('-')[0]
    return TIMESLOT_PREFIX_TO_DAY_INDEX[timeslot_day_prefix]

def remove_match_from_day(matches, removed_match_id):

    final_matches = []
    for match_id in matches:
        if match_id == removed_match_id:
            continue
        final_matches.append(match_id)

    return final_matches

async def notify_both_teams_about_unschedule(client, db, matchup, team_name_removed):

    context = matchup['context']

    team_owners_channel = get_team_owners_channel_from_context(client, context)

    league_teams = get_league_teams_collection_from_context(db, context)
    team1 = league_teams.find_one({'team_name': matchup['team1']})
    team2 = league_teams.find_one({'team_name': matchup['team2']})

    team_1_role_id = team1['team_role_id']
    team_2_role_id = team2['team_role_id']

    team_1_mention = f'<@&{team_1_role_id}>'
    team_2_mention = f'<@&{team_2_role_id}>'

    info_string = f'Your match for this week has been unscheduled by {team_name_removed}. Please reschedule it as soon as possible.'

    await safe_send(team_owners_channel, f'{team_1_mention} {team_2_mention} {info_string}', True)

async def unschedule_handler(db, message, client, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await safe_send(message.channel, 'You are not an admin of a league team.')
        return
    
    matchups = db['matchups']
    my_matchup = get_team_matchup(matchups, team_name, context)
    if not my_matchup:
        await safe_send(message.channel, 'Could not find a current matchup for your team.')
        return
    
    if my_matchup['timeslot'] == 'NONE':
        await safe_send(message.channel, 'Your match for this week is not currently scheduled yet.')
        return
    old_timeslot = my_matchup['timeslot']
    
    # get schedule plan
    
    schedule_plans = db['schedule_plans']
    season_schedule_plan = schedule_plans.find_one({'context': context, 'season': my_matchup['season']})

    if not season_schedule_plan:
        await safe_send(message.channel, 'Something went wrong, could not find this season.')
        return

    # ensure week plan is scheduling state

    week_index = season_schedule_plan['current_week']
    current_week = season_schedule_plan['weeks'][week_index]
    if current_week['status'] != 'SCHEDULING':
        await safe_send(message.channel, 'Scheduling is not currently open as this time.')
        return

    # get schedule object

    schedule_db = db['schedule']
    season_schedule = schedule_db.find_one({'context': context, 'season': my_matchup['season']})
    schedule_week = season_schedule['weeks'][week_index]
    day_index = get_day_index_from_timeslot(old_timeslot)

    # remove match id from schedule

    schedule_day = schedule_week['days'][day_index]
    updated_day_matches = remove_match_from_day(schedule_day['matches'], my_matchup['matchup_id'])
    schedule_day['matches'] = updated_day_matches
    schedule_db.update_one({'_id': season_schedule['_id']}, {'$set': {'weeks': season_schedule['weeks']}})

    my_team_index = get_team_index(team_name, my_matchup)

    matchups.update_one({'_id': my_matchup['_id']}, {'$set': {'team'+str(my_team_index)+'_timeslot': 'NONE', 'timeslot': 'NONE', 'added_to_schedule': False, 'weekday': 'NONE'}})

    await notify_both_teams_about_unschedule(client, db, my_matchup, team_name)
    await safe_send(message.channel, 'You have unscheduled your match for this week. Please reschedule it as soon as possible.')