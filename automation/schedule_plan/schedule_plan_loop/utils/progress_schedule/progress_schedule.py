

from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_status_of_not_started_week import check_status_of_not_started_week


async def progress_schedule(schedule_plans, schedule, message, client):

    current_week = schedule['current_week']
    week = schedule['weeks'][current_week]

    week_status = week['status']
    if week_status == 'NOT STARTED':
        await check_status_of_not_started_week(schedule_plans, schedule, week, message, current_week)