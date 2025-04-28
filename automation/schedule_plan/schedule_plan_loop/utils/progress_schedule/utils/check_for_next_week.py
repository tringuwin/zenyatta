

import constants

async def check_for_next_week(schedule_plans, schedule, message, current_week):

    total_weeks = len(schedule['weeks'])
    if current_week == total_weeks - 1:
        await message.channel.send(constants.STAFF_PING+' All weeks are complete in schedule play with context: '+schedule['context']+' and season: '+str(schedule['season'])+'.')
        return
    
    next_week = current_week + 1
    schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"current_week": next_week}})

    await message.channel.send(f'Week {next_week + 1} of schedule play with context: {schedule["context"]} and season: {schedule["season"]} has been set as active week.')