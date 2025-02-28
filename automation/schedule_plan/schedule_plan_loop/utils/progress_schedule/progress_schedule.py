

from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_if_matches_are_set import check_if_matches_are_set
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_match_scheduling_status import check_match_scheduling_status
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_status_of_matches import check_status_of_matches
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_status_of_not_started_week import check_status_of_not_started_week


async def progress_schedule(db, schedule_plans, schedule, message, client):

    current_week = schedule['current_week']
    week = schedule['weeks'][current_week]

    week_status = week['status']
    if week_status == 'NOT STARTED':
        await check_status_of_not_started_week(schedule_plans, schedule, week, message, current_week)
    elif week_status == 'MATCHUPS':
        await check_if_matches_are_set(client, db, schedule_plans, schedule, message, current_week)
    elif week_status == 'SCHEDULING':
        await check_match_scheduling_status(client, message, db, schedule_plans, schedule, week, current_week)
    elif week_status == 'MATCHES':
        await check_status_of_matches(db, message, schedule_plans, schedule)