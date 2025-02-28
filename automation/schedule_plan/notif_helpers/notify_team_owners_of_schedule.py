

from context.context_helpers import get_league_teams_collection_from_context, get_team_owners_channel_from_context


async def notify_team_owners_of_schedule(client, db, schedule, week_index, all_matchups):

    actual_week = week_index + 1
    context = schedule['context']
    
    team_owners_channel = get_team_owners_channel_from_context(client, context)
    league_teams = get_league_teams_collection_from_context(db, context)

