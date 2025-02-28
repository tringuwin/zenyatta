
from context.context_helpers import get_league_teams_collection_from_context, get_team_owners_channel_from_context


async def notify_team_owners_of_matches(client, db, matchups, context, week_number):

    team_owners_channel = get_team_owners_channel_from_context(client, context)
    league_teams = get_league_teams_collection_from_context(db, context)

    matchups_message = f'MATCHUPS FOR WEEK {week_number}\n'
    all_team_pings = ''

    for matchup in matchups:
        matchups_message += f'\n{matchup["team1"]} VS {matchup["team2"]}'

        team1 = league_teams.find_one({'team_name': matchup['team1']})
        team2 = league_teams.find_one({'team_name': matchup['team2']})

        team_1_ping = '<@&'+team1['team_role_id']+'>'
        team_2_ping = '<@&'+team2['team_role_id']+'>'

        all_team_pings += f'{team_1_ping} {team_2_ping} '

    matchups_message += '\n\nPlease ensure these matches are scheduled by Tuesday at midnight EST.'
    matchups_message += '\n\n'+all_team_pings

    await team_owners_channel.send(matchups_message)


