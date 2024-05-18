import constants

async def league_xp_handler(db, message, client):

    constants_db = db['constants']
    league_xp_obj = constants_db.find_one({'name': 'league_xp'})
    league_xp = league_xp_obj['value']

    sorted_list = sorted(league_xp.items(), key=lambda item: item[1], reverse=True)

    final_string = '**LEAGUE XP STANDINGS:**'

    guild = client.get_guild(constants.GUILD_ID)


    index = 1
    for team, xp in sorted_list:
        team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team]
        team_emoji = guild.get_emoji(team_emoji_id)
        final_string += '\n' + str(index)+'. '+str(team_emoji)+' '+team+': '+str(xp)+' XP'

        index += 1

    await message.channel.send(final_string)