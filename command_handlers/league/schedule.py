
current_season = 1
import constants
from discord_actions import get_guild

def team_name_to_emoji(team_name, guild):
    
    team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_name]
    team_emoji = guild.get_emoji(team_emoji_id)
    return team_emoji


async def schedule_handler(db, message, client):

    schedule = db['schedule']
    season_schedule = schedule.find_one({'season': current_season})

    guild = await get_guild(client)

    final_string = '**~ LEAGUE SCHEDULE ~**'
    for week in season_schedule['weeks']:

        final_string += '\n----------------'
        final_string += '\n**WEEK '+str(week['week'])+' - '+week['date']+' - 3:00 PM EST**'
        for match in week['matches']:
            team1 = match[0]
            team2 = match[1]

            team1_emoji = team_name_to_emoji(team1, guild)
            team2_emoji = team_name_to_emoji(team2, guild)

            final_string += '\n'+str(team1_emoji)+' **'+team1+'** VS '+str(team2_emoji)+' **'+team2+'**'

    await message.channel.send(final_string)


