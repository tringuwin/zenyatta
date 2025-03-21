import constants
from discord_actions import get_guild
from helpers import get_league_emoji_from_team_name

POWER_RANKINGS = [

    'Phantoms',
    'Lotus',
    'Evergreen',
    'Polar',
    'Horizon',
    'Hunters',
    'Legion',
    'Fresas',
    'Outliers',
    'Monarchs',
    'Deadlock',
    'Olympians',
    'Ragu',
    'Phoenix',
    'Eclipse',
    'Guardians',
    'Misfits',
    'Saturn',
    'Diamonds',
    'Angels',
    'Celestials',
    'Sentinels',
    'Saviors',
    'Instigators',

]

LAST_UPDATED = '12/3/2024 2:00 AM ET'

async def power_rankings_handler(message, client):

    # await message.channel.send('Power rankings will return after SOL Week 1 concludes!')
    # return

    guild = await get_guild(client)

    final_string = '**CURRENT SOL POWER RANKINGS**'

    team_index = 1
    for team in POWER_RANKINGS:

        emoji_string = get_league_emoji_from_team_name(team)

        final_string += '\n'+str(team_index)+'. '+emoji_string+' '+team

        team_index += 1

    final_string += '\n\n*Based off of rosters and limited knowledge. May be very innacurate, take with a grain of salt*'
    final_string += '\n**Last Updated: '+LAST_UPDATED+'**'

    await message.channel.send(final_string)

