import constants
from discord_actions import get_guild

POWER_RANKINGS = [

    'Phantoms',
    'Hunters',
    'Lotus',
    'Polar',
    'Sentinels',
    'Outliers',
    'Fresas',
    'Monarchs',
    'Horizon',
    'Ragu',
    'Evergreen',
    'Misfits',
    'Phoenix',
    'Legion',
    'Deadlock',
    'Angels',
    'Eclipse',
    'Olympians',
    'Saturn',
    'Celestials',
    'Guardians',
    'Saviors',
    'Diamonds',
    'Instigators',

]

LAST_UPDATED = '10/20/2024 1:17 AM EST'

async def power_rankings_handler(message, client):

    guild = await get_guild(client)

    final_string = '**CURRENT SOL POWER RANKINGS**'

    team_index = 1
    for team in POWER_RANKINGS:

        team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team]
        team_emoji = guild.get_emoji(team_emoji_id)

        final_string += '\n'+str(team_index)+'. '+str(team_emoji)+' '+team

        team_index += 1

    final_string += '\n\n*Based off of rosters and limited scrim/match knowledge. May be very innacurate,  take with a grain of salt*'
    final_string += '\n**Last Updated: '+LAST_UPDATED+'**'

    await message.channel.send(final_string)

