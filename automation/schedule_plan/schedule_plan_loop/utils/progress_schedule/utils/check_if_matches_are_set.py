


async def check_if_matches_are_set(db, schedule_plans, schedule, week, message, current_week):

    actual_week = current_week + 1
    league_context = schedule['context']