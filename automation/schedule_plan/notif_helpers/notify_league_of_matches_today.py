
import constants
from context.context_helpers import get_league_announcements_channel_from_context


async def notify_league_of_matches_today(client, context, matchups_today):

    announcements_channel = get_league_announcements_channel_from_context(client, context)

    announcement_message = constants.LEAGUE_NOTIFS_MENTION+'\n\n**LEAGUE MATCHES SCHEDULED FOR TODAY**\n\n'

    for matchup in matchups_today:
        team1_name = matchup['team1']
        team2_name = matchup['team2']

        timeslot = matchup['timeslot']
        match_time_number = int(timeslot.split('-')[1])
        match_time = f'{match_time_number}:00 PM EST'

        announcement_message += f'{match_time} - **{team1_name}** VS **{team2_name}**\n'

    await announcements_channel.send(announcement_message)

    
        

    
