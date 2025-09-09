

from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_day_progress import check_day_progress
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.check_if_day_has_started import check_if_day_has_started
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.complete_finished_matchups import complete_finished_matchups
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.get_all_matchups import get_all_matchups
from safe_send import safe_send



async def check_status_of_matches(client, db, message, schedule_plans, schedule):

    context = schedule['context']
    season = schedule['season']
    week_index = schedule['current_week']
    actual_week = week_index + 1

    all_matchups = get_all_matchups(db, context, season, actual_week)
    not_completed_matchups = complete_finished_matchups(db, all_matchups, context, season)
    all_matches_completed = len(not_completed_matchups) == 0
    await safe_send(message.channel, f'Matches not completed for context {context} is {len(not_completed_matchups)}.')

    if all_matches_completed:
        schedule['weeks'][week_index]['status'] = 'COMPLETE'
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})
        await safe_send(message.channel, f'Matchups are complete for week {actual_week} of season {season} of league {context}.')
        return
    
    season_week = schedule['weeks'][week_index]
    week_day_index = season_week['day_number']
    current_day = season_week['days'][week_day_index]
    current_day_status = current_day['status']

    if current_day_status == 'NOT STARTED':
        await check_if_day_has_started(current_day['date'], schedule, schedule_plans, week_index, week_day_index)
    elif current_day_status == 'IN PROGRESS':
        await check_day_progress(client, db, season_week, week_day_index, week_index, schedule, schedule_plans)

    
