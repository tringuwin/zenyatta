

from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.get_all_matchups import get_all_matchups
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.save_matchups_to_history import save_matchups_to_history


def all_matches_completed(all_matches):

    for match in all_matches:
        if not match['match_over']:
            return False

    return True


async def check_status_of_matches(db, message, schedule_plans, schedule):

    context = schedule['context']
    season = schedule['season']
    week_index = schedule['current_week']
    actual_week = week_index + 1

    all_matches = get_all_matchups(db, context, season, actual_week)
    all_matches_completed = all_matches_completed(all_matches)

    if all_matches_completed:
        save_matchups_to_history(db, all_matches)
        schedule['weeks'][week_index]['status'] = 'COMPLETE'
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})
        await message.channel.send(f'Matchups are complete for week {actual_week} of season {season} of league {context}.')
        return