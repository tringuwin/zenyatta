

async def noon_match_notify(client, context, db, season, week_index, day_index):

    schedule_db = db['schedule']
    season_schedule = schedule_db.find_one({"season": season, "context": context})

    day_in_schedule = season_schedule['weeks'][week_index]['days'][day_index]

    #league_announcements_channel = get_league_announcements_channel_from_context(client, context)