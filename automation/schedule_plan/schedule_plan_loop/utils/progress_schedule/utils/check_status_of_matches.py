

from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.complete_finished_matchups import complete_finished_matchups
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.get_all_matchups import get_all_matchups



async def check_status_of_matches(db, message, schedule_plans, schedule):

    return

    context = schedule['context']
    season = schedule['season']
    week_index = schedule['current_week']
    actual_week = week_index + 1

    all_matchups = get_all_matchups(db, context, season, actual_week)
    not_completed_matchups = complete_finished_matchups(db, all_matchups, context, season)
    all_matches_completed = len(not_completed_matchups) == 0

    if all_matches_completed:
        schedule['weeks'][week_index]['status'] = 'COMPLETE'
        new_week_index = week_index + 1
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks'], "current_week": new_week_index}})
        await message.channel.send(f'Matchups are complete for week {actual_week} of season {season} of league {context}.')
        return
    
