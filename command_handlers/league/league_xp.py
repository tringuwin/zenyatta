

async def league_xp_handler(db, message, client):

    constants_db = db['constants']
    league_xp_obj = constants_db.find_one({'name': 'league_xp'})
    league_xp = league_xp_obj['value']

    sorted_list = sorted(league_xp.items(), key=lambda item: item[1])

    final_string = '**LEAGUE XP STANDINGS:**'

    for team, xp in sorted_list:
        final_string += '\n'+team+': '+str(xp)+' XP'

    await message.channel.send(final_string)