

from automation.schedule_plan.notif_helpers.notify_staff_for_matches import notify_staff_for_matches
from time_helpers import has_date_passed_est


async def check_status_of_not_started_week(schedule_plans, schedule, week, message, week_index):

    first_day_of_week = week['days'][0]
    first_day_date = first_day_of_week['date']

    has_week_started = has_date_passed_est(first_day_date['day'], first_day_date['month'], first_day_date['year'])

    if has_week_started:
        schedule['weeks'][week_index]['status'] = 'MATCHUPS'
        schedule_plans.update_one({'_id': schedule['_id']}, {'$set': {'weeks': schedule['weeks']}})
        await message.channel.send(f'Week has started for league with context {schedule["context"]} for season {schedule["season"]}')
        await notify_staff_for_matches(message, schedule)
    else:
        await message.channel.send(f'Week has not started yet for league with context {schedule["context"]} for season {schedule["season"]}')
        return
