

from automation.schedule_plan.schedule_plan_loop.utils.check_for_schedule_start import check_for_schedule_start
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.progress_schedule import progress_schedule


async def schedule_plan_loop(db, message, client):

    schedule_plans = db['schedule_plans']
    all_schedules = schedule_plans.find()

    for schedule in all_schedules:
        if schedule['status'] == 'NOT STARTED':
            await check_for_schedule_start(schedule_plans, schedule, message)
        elif schedule['status'] == 'IN PROGRESS':
            await progress_schedule(schedule_plans, schedule, message, client)

    
