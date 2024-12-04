import constants
from helpers import get_constant_value, set_constant_value


async def general_league_xp(db, message, client, start_string, constant_name):

    constants_db = db['constants']
    league_xp_obj = constants_db.find_one({'name': constant_name})
    league_xp = league_xp_obj['value']

    sorted_list = sorted(league_xp.items(), key=lambda item: item[1], reverse=True)

    final_string = start_string

    index = 1
    for team, xp in sorted_list:
        team_emoji_string = constants.TEAM_NAME_TO_EMOJI_EMBED_STRING[team]
        final_string += '\n' + str(index)+'. '+team_emoji_string+' '+team+': '+str(xp)+' XP'

        index += 1

    await message.channel.send(final_string)



async def league_xp_handler(db, message, client):

    await general_league_xp(db, message, client, '**MONTHLY LEAGUE XP STANDINGS:**', 'league_xp')


async def total_league_xp_handler(db, message, client):

    await general_league_xp(db, message, client, '**ALL-TIME LEAGUE XP STANDINGS:**', 'league_xp_total')


async def wipe_league_xp_handler(db, message):

    league_xp_obj = get_constant_value(db, 'league_xp')

    for team in league_xp_obj:
        league_xp_obj[team] = 0

    set_constant_value(db, 'league_xp', league_xp_obj)

    await message.channel.send('Monthly League XP wiped.')

    

