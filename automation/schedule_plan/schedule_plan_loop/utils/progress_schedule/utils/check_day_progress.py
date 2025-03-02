

from automation.schedule_plan.notif_helpers.notify_league_of_matches_today import notify_league_of_matches_today
from time_helpers import has_date_passed_est, is_after_noon_est


async def check_day_progress(season_week, day_index, week_index, schedule, schedule_plans):
    
    if day_index != 6:
        next_day_index = day_index + 1
        next_day = season_week['days'][next_day_index]
        next_day_date = next_day['date']
        next_day_started = has_date_passed_est(next_day_date['day'], next_day_date['month'], next_day_date['year'])

        if next_day_started:
            schedule['weeks'][week_index]['day_number'] = next_day_index
            schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})
            return
        
    season_day = season_week['days'][day_index]
    
    if (not season_day['notified']):
        if is_after_noon_est():

            # notify team owners with matches today
            await notify_league_of_matches_today()

            schedule['weeks'][week_index]['days'][day_index]['notified'] = True
            schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})