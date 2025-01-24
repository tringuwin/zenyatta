

import constants
from helpers import get_constant_value, get_league_emoji_from_team_name


async def schedule_handler(db, message, client):

    # final_string = "**SEASON 3 PLAYOFF SCHEDULE**"

    # final_string += '\n\n**Saturday, July 20th | Grand-Finals**'
    # final_string += '\nMATCH 1: <:misfits:1237197162354446336> **Misfits** VS <:saviors:1176588866828914748> **Saviors**'
    # final_string += '\n\n**Sunday, July 21st | Grand-Finals**'
    # final_string += '\nMATCH 1: <:hunters:1245542818731134976> **Hunters** VS <:eclipse:1174517640987938926> **Eclipse**'
    # final_string += '\nMATCH 2: <:outliers:1200928308922167357> **Outliers** VS <:evergreen:1241087086207959040> **Evergreen**'

    # final_string = '**GRAND FINALS : Sunday 5/5/2024 at 4:30 PM EST**'
    # final_string += '\nFresas VS Olympians'

    # await message.channel.send(final_string)

    league_season = get_constant_value(db, 'league_season')
    league_week = get_constant_value(db, 'league_week')

    schedule = db['schedule']
    season_schedule = schedule.find_one({'season': league_season})

    weeks = 0
    week_index = 1
    total_matches_added = 0
    for week in season_schedule['weeks']:

        if week_index < league_week:
            week_index += 1
            continue

        final_string = '\n**SEASON 4 WEEK '+str(week['week'])+'**'

        for day in week['days']:

            if len(day['matches']) < 1:
                continue

            final_string += '\n\n**'+day['date']+'**'
            final_string += '\n------------------'
            match_index = 1

            for match in day['matches']:
                match_time = match['time']
                home_team = match['home']
                away_team = match['away']

                home_emoji_string = get_league_emoji_from_team_name(home_team)
                away_emoji_string = get_league_emoji_from_team_name(away_team)
                # final_string += '\n'+date
                match_string = "Match "+str(match_index)+' : '+match_time+' EST : '
                teams_string = home_emoji_string+' **'+home_team+'** VS '+away_emoji_string+' **'+away_team+'**'
                final_string += '\n'+match_string+teams_string

                match_index += 1
                total_matches_added += 1

        week_index += 1
        weeks += 1
        if weeks == 1:
            break

    if total_matches_added == 0:
        final_string += '\n\nLooks like the matches for this week have not been added yet. They usually appear on Wednesday. Check back soon!'

    final_string += f'\n\nSee the full Schedule here: {constants.WEBSITE_DOMAIN}/sol/schedule'

    await message.channel.send(final_string)


