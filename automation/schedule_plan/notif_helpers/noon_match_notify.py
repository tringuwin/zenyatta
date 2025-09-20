

from automation.schedule_plan.notif_helpers.notify_league_of_matches_today import notify_league_of_matches_today
from automation.schedule_plan.notif_helpers.notify_team_owners_with_matches_today import notify_team_owners_with_matches_today


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
        if match:
            matchups_today.append(match)

    sorted_matchups_today = sorted(matchups_today, key=lambda x: int(x['match_epoch']))

    await notify_league_of_matches_today(client, context, sorted_matchups_today)
    await notify_team_owners_with_matches_today(client, db, context, sorted_matchups_today)