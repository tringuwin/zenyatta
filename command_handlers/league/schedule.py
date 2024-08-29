

import constants
from discord_actions import get_guild

def team_name_to_emoji(team_name, guild):
    
    team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_name]
    team_emoji = guild.get_emoji(team_emoji_id)
    return team_emoji


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

    schedule = db['schedule']
    season_schedule = schedule.find_one({'season': constants.LEAGUE_SEASON})

    guild = await get_guild(client)

    final_string = '**~ LEAGUE SCHEDULE ~**'
    weeks = 0
    for week in season_schedule['weeks']:


        final_string += '\n----------------'
        final_string += '\n**WEEK '+str(week['week'])+'**'

        for day in week['days']:

            final_string += '\n----------------'
            final_string += '\n**'+week['date']+'**'

            for match in day['matches']:
                match_time = match['time']
                home_team = match['home']
                away_team = match['away']

                home_emoji = team_name_to_emoji(home_team, guild)
                away_emoji = team_name_to_emoji(away_team, guild)
                # final_string += '\n'+date
                final_string += '\n'+str(home_emoji)+' **'+home_team+'** VS '+str(away_emoji)+' **'+away_team+'**'

        weeks += 1
        if weeks == 2:
            break

    final_string += '\n----------------'
    final_string += '\n5 Total Weeks in the Regular Season'
    final_string += '\nSee the full Schedule here: https://spicyragu.netlify.app/sol/schedule'

    await message.channel.send(final_string)


