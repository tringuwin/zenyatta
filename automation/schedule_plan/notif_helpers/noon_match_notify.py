

from automation.schedule_plan.notif_helpers.notify_league_of_matches_today import notify_league_of_matches_today


async def noon_match_notify(client, context, db, season, week_index, day_index):

    schedule_db = db['schedule']
    season_schedule = schedule_db.find_one({"season": season, "context": context})

    day_in_schedule = season_schedule['weeks'][week_index]['days'][day_index]
    match_ids_today = day_in_schedule['matches']

    if len(match_ids_today) == 0:
        return
    
    matchups_today = []
    matchups = db['matchups']
    for match_id in match_ids_today:
        match = matchups.find_one({"matchup_id": match_id})
        matchups_today.append(match)

    await notify_league_of_matches_today(client, context, matchups_today)
    # notify team owners with matches today