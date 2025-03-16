

from context.context_helpers import get_league_teams_collection_from_context, get_team_owners_channel_from_context


async def notify_team_owners_with_matches_today(client, db, context, matchups_today):

    team_owners_channel = get_team_owners_channel_from_context(client, context)
    league_teams = get_league_teams_collection_from_context(db, context)

    team_pings = ''

    for matchup in matchups_today:
        
        team1 = league_teams.find_one({'team_name': matchup['team1']})
        team2 = league_teams.find_one({'team_name': matchup['team2']})

        team_1_ping = '<@&'+str(team1['team_role_id'])+'>'
        team_2_ping = '<@&'+str(team2['team_role_id'])+'>'

        team_pings += f'{team_1_ping} {team_2_ping} '

    playing_today_message = 'Your team has a match today. Please make sure your team is ready to play by the match time.'
    if context == 'OW':
        playing_today_message += '\n\nPlease make sure the lineup for your team has been set prior to the match. Use the command **!setlineup** to set your lineup.'

    await team_owners_channel.send(f'{team_pings}\n\n{playing_today_message}')