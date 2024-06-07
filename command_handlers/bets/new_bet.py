

from discord_actions import get_guild
import constants

async def new_bet_handler(db, message, client):

    bet_parts = message.content.split('|')
    if len(bet_parts) != 4:
        await message.channel.send('4 arguments required')
        return
    
    team_1_name = bet_parts[2]
    team_2_name = bet_parts[3]

    teams = db['leagueteams']

    team_1 = teams.find_one({'name_lower': team_1_name.lower()})
    if not team_1:
        await message.channel.send(team_1_name+' is not a valid team name')
        return
    team_2 = teams.find_one({'name_lower': team_2_name.lower()})
    if not team_2:
        await message.channel.send(team_2_name+' is not a valid team name')
        return

    guild = await get_guild(client)
    bet_channel = guild.get_channel(constants.BET_CHANNEL_ID)

    title = bet_parts[1]
    await bet_channel.send(title)

    bets = db['bets']
