

from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.force_scheduling import force_scheduling
from time_helpers import has_date_passed_est


async def not_scheduled_action(db, schedule_plans, schedule, week, week_index, all_matchups):
    
    wednesday_of_week = week['days'][2]
    wednesday_date = wednesday_of_week['date']
    wednesday_has_passed = has_date_passed_est(wednesday_date['day'], wednesday_date['month'], wednesday_date['year'])

    if wednesday_has_passed:
        await force_scheduling(db, schedule_plans, schedule, week_index, all_matchups)
        return

    #applicable_warning = get_applicable_warning(week, wednesday_datetime)