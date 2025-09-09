

import constants
from safe_send import safe_send

async def check_for_next_week(schedule_plans, schedule, message, current_week):

    total_weeks = len(schedule['weeks'])
    if current_week == total_weeks - 1:
        await safe_send(message.channel, 'All weeks are complete in schedule plan with context: '+schedule['context']+' and season: '+str(schedule['season'])+'.')
        return
    
    next_week = current_week + 1
    schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"current_week": next_week}})

    await safe_send(message.channel, f'Week {next_week + 1} of schedule plan with context: {schedule["context"]} and season: {schedule["season"]} has been set as active week.')