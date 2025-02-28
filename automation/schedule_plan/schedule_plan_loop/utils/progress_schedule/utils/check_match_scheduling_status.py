

from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.get_all_matchups import get_all_matchups


def do_all_matchups_have_timeslot(all_matchups):

    for matchup in all_matchups:
        if matchup['timeslot'] == 'NONE':
            return False
    
    return True


async def check_match_scheduling_status(message, db, schedule_plans, schedule, week, week_index):

    actual_week = schedule['current_week'] + 1

    all_matchups = get_all_matchups(db, schedule['context'], schedule['season'], actual_week)
    all_matchups_have_timeslot = do_all_matchups_have_timeslot(all_matchups)

    if all_matchups_have_timeslot:
        schedule['weeks'][week_index]['status'] = 'MATCHES'
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})
        await message.channel.send(f'Match scheduling is complete for week {actual_week} of season {schedule["season"]} of league {schedule["context"]}.')
        return

    current_day_index = week['day_number']
    current_day = week['days'][current_day_index]
    current_day_status = current_day['status']



