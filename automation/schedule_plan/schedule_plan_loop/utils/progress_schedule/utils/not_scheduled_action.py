
from automation.schedule_plan.notif_helpers.notify_team_owners_schedule_warning import notify_team_owners_schedule_warning
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.force_scheduling import force_scheduling
from time_helpers import get_datetime_now_est, has_date_passed_est, year_month_day_to_datetime


SECONDS_IN_A_DAY = 86400
SECONDS_IN_5_HOURS = 18000
SECONDS_IN_1_HOUR = 3600

def get_applicable_warning(week, wednesday_datetime):

    week_notifs = week['notifs']
    datetime_now = get_datetime_now_est()

    time_diff = wednesday_datetime - datetime_now
    time_diff_seconds = time_diff.total_seconds()

    if time_diff_seconds < 0:
        return False
    
    if time_diff_seconds < SECONDS_IN_1_HOUR and (not week_notifs['notified_1_hour_left']):
        return 'notified_1_hour_left'
    if time_diff_seconds < SECONDS_IN_5_HOURS and (not week_notifs['notified_5_hours_left']):
        return 'notified_5_hours_left'
    if time_diff_seconds < SECONDS_IN_A_DAY and (not week_notifs['notified_1_day_left']):
        return 'notified_1_day_left'
    return False


def get_teams_to_warn(all_matchups):

    teams_to_warn = []

    for matchup in all_matchups:

        if matchup['timeslot'] == 'NONE':
            teams_to_warn.append(matchup['team1'])
            teams_to_warn.append(matchup['team2'])

    return teams_to_warn
            

WARNING_KEY_TO_WARNING_TYPE = {
    'notified_1_hour_left': '1H',
    'notified_5_hours_left': '5H',
    'notified_1_day_left': '1D'
}

async def not_scheduled_action(client, db, schedule_plans, schedule, week, week_index, all_matchups):
    
    wednesday_of_week = week['days'][2]
    wednesday_date = wednesday_of_week['date']
    wednesday_has_passed = has_date_passed_est(wednesday_date['day'], wednesday_date['month'], wednesday_date['year'])

    if wednesday_has_passed:
        await force_scheduling(db, all_matchups)
        return

    wednesday_datetime = year_month_day_to_datetime(wednesday_date['year'], wednesday_date['month'], wednesday_date['day'])
    applicable_warning = get_applicable_warning(week, wednesday_datetime)
    teams_to_warn = get_teams_to_warn(all_matchups)

    if applicable_warning:
        
        await notify_team_owners_schedule_warning(client, db, schedule['context'], teams_to_warn, WARNING_KEY_TO_WARNING_TYPE[applicable_warning])

        schedule['weeks'][week_index]['notifs'][applicable_warning] = True
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})
