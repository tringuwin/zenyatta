

from automation.schedule_plan.notif_helpers.notify_team_owners_of_schedule import notify_team_owners_of_schedule
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.get_all_matchups import get_all_matchups
from automation.schedule_plan.schedule_plan_loop.utils.progress_schedule.utils.not_scheduled_action import not_scheduled_action


def do_all_matchups_have_timeslot(all_matchups):

    for matchup in all_matchups:
        if matchup['timeslot'] == 'NONE':
            return False
    
    return True

TIMESLOT_DAY_TO_DAY_INDEX = {
    'W': 2,
    'T': 3,
    'F': 4,
    'S': 5,
    'X': 6,
}

def write_matchups_to_schedule(db, schedule_plan, all_matchups):
    print('writing matches to schedule')
    print('input matchups', all_matchups)
    schedule_db = db['schedule']
    schedule_edited = False
    this_season_schedule = schedule_db.find_one({'context': schedule_plan['context'], 'season': schedule_plan['season']})
    week_index = schedule_plan['current_week']

    for matchup in all_matchups:
        if (not matchup['added_to_schedule']) and matchup['timeslot'] != 'NONE':

            timeslot_parts = matchup['timeslot'].split('-')
            timeslot_day = timeslot_parts[0]
            timeslot_day_index = TIMESLOT_DAY_TO_DAY_INDEX[timeslot_day]

            this_season_schedule['weeks'][week_index]['days'][timeslot_day_index]['matches'].append(matchup['matchup_id'])
            schedule_edited = True
            matchup['added_to_schedule'] = True
            
    if schedule_edited:
        schedule_db.update_one({'_id': this_season_schedule['_id']}, {'$set': {'weeks': this_season_schedule['weeks']}})

    print('output matchups', all_matchups)
    return all_matchups


async def check_match_scheduling_status(client, message, db, schedule_plans, schedule, week, week_index):

    actual_week = schedule['current_week'] + 1

    all_matchups = get_all_matchups(db, schedule['context'], schedule['season'], actual_week)
    all_matchups = write_matchups_to_schedule(db, schedule, all_matchups)
    all_matchups_have_timeslot = do_all_matchups_have_timeslot(all_matchups)

    if all_matchups_have_timeslot:

        await notify_team_owners_of_schedule(client, db, schedule, all_matchups)

        schedule['weeks'][week_index]['status'] = 'MATCHES'
        schedule_plans.update_one({"_id": schedule['_id']}, {"$set": {"weeks": schedule['weeks']}})
        await message.channel.send(f'Match scheduling is complete for week {actual_week} of season {schedule["season"]} of league {schedule["context"]}.')
        return
    
    await not_scheduled_action(client, db, schedule_plans, schedule, week, week_index, all_matchups)



