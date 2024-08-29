

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
    index = 1
    weeks = 0
    for week in season_schedule['weeks']:

        if index < constants.LEAGUE_WEEK:
            index += 1
            continue


        final_string += '\n----------------'
        final_string += '\n**WEEK '+str(week['week'])+'**'
        for match in week['matches']:
            # date = match[0]
            team1 = match[1]
            team2 = match[2]

            team1_emoji = team_name_to_emoji(team1, guild)
            team2_emoji = team_name_to_emoji(team2, guild)
            # final_string += '\n'+date
            final_string += '\n'+str(team1_emoji)+' **'+team1+'** VS '+str(team2_emoji)+' **'+team2+'**'

        index += 1
        weeks += 1
        if weeks == 3:
            break

    final_string += '\n----------------'
    final_string += '\n5 Total Weeks in the Regular Season'
    final_string += '\nSee the full Schedule here: https://spicyragu.netlify.app/sol/schedule'

    await message.channel.send(final_string)


