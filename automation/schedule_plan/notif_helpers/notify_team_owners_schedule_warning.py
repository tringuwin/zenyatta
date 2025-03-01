

from context.context_helpers import get_league_teams_collection_from_context, get_team_owners_channel_from_context

WARNING_TYPE_TO_MESSAGE = {
    '1H': '1 hour',
    '5H': '5 hours',
    '1D': '1 day'
}


async def notify_team_owners_schedule_warning(client, db, context, teams_to_warn, warning_type):

    team_owners_channel = get_team_owners_channel_from_context(client, context)
    league_teams = get_league_teams_collection_from_context(db, context)

    warning_text_from_time = WARNING_TYPE_TO_MESSAGE[warning_type] 
    Warning_message = f'This is a warning that there is less than {warning_text_from_time} to schedule your match for this week. Please make sure matches are scheduled by **Tuesday at Midnight** otherwise a timeslot will be automatically assigned.\n\n'
    all_team_pings = ''

    for team_name in teams_to_warn:
        team = league_teams.find_one({'team_name': team_name})
        team_ping = '<@&'+str(team['team_role_id'])+'>'
        all_team_pings += f'{team_ping} '

    await team_owners_channel.send(Warning_message + all_team_pings)