

from time_helpers import has_date_passed_est


async def check_for_schedule_start(schedule_plans, schedule, message):
    
    first_day_of_schedule = schedule['weeks'][0]['days'][0]
    first_day_date = first_day_of_schedule['date']
    
    has_season_started = has_date_passed_est(first_day_date['day'], first_day_date['month'], first_day_date['year'])

    if has_season_started:
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"status": "IN PROGRESS"}})
        await message.channel.send(f"Season {schedule['season']} of league {schedule['context']} has started!")
        return

    await message.channel.send(f"Season {schedule['season']} of league {schedule['context']} has not started yet.")
    