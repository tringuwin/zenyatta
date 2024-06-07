

from discord_actions import get_guild
import constants
import discord

from league import get_team_color_by_name

async def new_bet_handler(db, message, client):

    bet_parts = message.content.split('|')
    if len(bet_parts) != 5:
        await message.channel.send('5 arguments required')
        return
    
    home_away_bool = bet_parts[4]
    uses_home_away = False
    if home_away_bool != '0' and home_away_bool != '1':
        await message.channel.send('Last argument must be 0 or 1')
        return
    
    if home_away_bool == '1':
        uses_home_away = True

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
    
    team_1_name = team_1['team_name']
    team_2_name = team_2['team_name']


    guild = await get_guild(client)
    bet_channel = guild.get_channel(constants.BET_CHANNEL_ID)

    title = bet_parts[1]
    await bet_channel.send(title)


    team_1_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_1_name]
    team_1_emoji = guild.get_emoji(team_1_emoji_id)

    team_2_emoji_id = constants.LEAGUE_TO_EMOJI_ID[team_2_name]
    team_2_emoji = guild.get_emoji(team_2_emoji_id)

    team_1_embed = discord.Embed(title='HOME TEAM: '+str(team_1_emoji)+' '+team_1_name, color=get_team_color_by_name(team_1_name))
    await bet_channel.send(embed=team_1_embed)
    team_2_embed = discord.Embed(title='AWAY TEAM: '+str(team_2_emoji)+' '+team_2_name, color=get_team_color_by_name(team_2_name))
    await bet_channel.send(embed=team_2_embed)



    bets = db['bets']

    await message.channel.send('Bet created.')
