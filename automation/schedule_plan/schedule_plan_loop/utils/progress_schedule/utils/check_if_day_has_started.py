

from time_helpers import has_date_passed_est


async def check_if_day_has_started(date, schedule, schedule_plans, week_index, day_index):
    
    has_today_started = has_date_passed_est(date['day'], date['month'], date['year'])
    if has_today_started:
        schedule['weeks'][week_index]['days'][day_index]['status'] = 'IN PROGRESS'
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})