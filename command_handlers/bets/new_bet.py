

import time
from discord_actions import get_guild
import constants
import discord

from helpers import get_league_emoji_from_team_name
from league import get_team_color_by_name, get_team_record_string
from safe_send import safe_send_embed


async def new_bet(client, db, title, team_1_name, team_2_name, uses_home_away, timestamp=None):

    guild = await get_guild(client)
    bet_channel = guild.get_channel(constants.BET_CHANNEL_ID)

    title_msg = await bet_channel.send('**'+title+'**')

    team_1_emoji_string = get_league_emoji_from_team_name(team_1_name)
    team_2_emoji_string = get_league_emoji_from_team_name(team_2_name)

    team_1_title = 'HOME TEAM: ' if uses_home_away else 'TEAM 1: '
    team_2_title = 'AWAY TEAM: ' if uses_home_away else 'TEAM 2: '

    team_1_embed = discord.Embed(title=team_1_title+team_1_emoji_string+' '+team_1_name, color=get_team_color_by_name(team_1_name))
    team_1_embed.add_field(name="Total Tokens Bet On Team", value="🪙 0", inline=False)
    team_1_embed.add_field(name="Current Payout Rate", value="1:1", inline=False)
    team_1_embed.add_field(name="Team Season Record", value=get_team_record_string(db, team_1_name), inline=False)
    team_1_embed.add_field(name="Command to Bet", value='!bet '+team_1_name+' [number of tokens]', inline=False)
    team_1_msg = await safe_send_embed(bet_channel, team_1_embed)

    team_2_embed = discord.Embed(title=team_2_title+team_2_emoji_string+' '+team_2_name, color=get_team_color_by_name(team_2_name))
    team_2_embed.add_field(name="Total Tokens Bet On Team", value="🪙 0", inline=False)
    team_2_embed.add_field(name="Current Payout Rate", value="1:1", inline=False)
    team_2_embed.add_field(name="Team Season Record", value=get_team_record_string(db, team_2_name), inline=False)
    team_2_embed.add_field(name="Command to Bet", value='!bet '+team_2_name+' [number of tokens]', inline=False)
    team_2_msg = await safe_send_embed(bet_channel, team_2_embed)

    bet_obj = {
        'bet_id': title_msg.id,
        'team_1_msg': team_1_msg.id,
        'team_2_msg': team_2_msg.id,
        'team_1': team_1_name,
        'team_2': team_2_name,
        'team_1_betters': {},
        'team_2_betters': {},
        'open': True,
        'uses_home_away': uses_home_away
    }

    if timestamp:
        bet_obj['timestamp'] = timestamp

    bets = db['bets']
    bets.insert_one(bet_obj)


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

    title = bet_parts[1]

    await new_bet(client, db, title, team_1_name, team_2_name, uses_home_away)

    await message.channel.send('Bet created.')


def total_tokens_on_team(betters):

    total = 0
    for better_id in betters:

        better = betters[better_id]
        total += better['tokens']

    return total


def get_team_payout_rate(my_total, other_total):

    if other_total == 0 or my_total == 0:
        return 1

    paid_per_token = other_total/my_total
    paid_per_token = float(paid_per_token) * 0.95
    paid_per_token += 1

    return round(paid_per_token, 3)

async def update_bets(db, channel, client):

    await channel.send('Starting to update bets')

    guild = await get_guild(client)
    bet_channel = guild.get_channel(constants.BET_CHANNEL_ID)

    bets = db['bets']
    all_bets = bets.find()
    for bet in all_bets:

        team_1_name = bet['team_1']
        team_1_emoji_string = get_league_emoji_from_team_name(team_1_name)
        team_1_total = total_tokens_on_team(bet['team_1_betters'])

        team_2_name = bet['team_2']
        team_2_emoji_string = get_league_emoji_from_team_name(team_2_name)
        team_2_total = total_tokens_on_team(bet['team_2_betters'])

        uses_home_away = bet['uses_home_away']
        team_1_title = 'HOME TEAM: ' if uses_home_away else 'TEAM 1: '
        team_2_title = 'AWAY TEAM: ' if uses_home_away else 'TEAM 2: '

        bet_msg_1 = await bet_channel.fetch_message(bet['team_1_msg'])
        new_embed_1 = discord.Embed(title=team_1_title+team_1_emoji_string+' '+team_1_name, color=get_team_color_by_name(team_1_name))
        new_embed_1.add_field(name="Total Tokens Bet On Team", value="🪙 "+str(team_1_total), inline=False)
        new_embed_1.add_field(name="Current Payout Rate", value="1:"+str(get_team_payout_rate(team_1_total, team_2_total)), inline=False)
        new_embed_1.add_field(name="Team Season Record", value=get_team_record_string(db, team_1_name), inline=False)
        new_embed_1.add_field(name="Command to Bet", value='!bet '+team_1_name+' [number of tokens]', inline=False)
        await bet_msg_1.edit(embed=new_embed_1, content='')

        bet_msg_2 = await bet_channel.fetch_message(bet['team_2_msg'])
        new_embed_2 = discord.Embed(title=team_2_title+team_2_emoji_string+' '+team_2_name, color=get_team_color_by_name(team_2_name))
        new_embed_2.add_field(name="Total Tokens Bet On Team", value="🪙 "+str(team_2_total), inline=False)
        new_embed_2.add_field(name="Current Payout Rate", value="1:"+str(get_team_payout_rate(team_2_total, team_1_total)), inline=False)
        new_embed_2.add_field(name="Team Season Record", value=get_team_record_string(db, team_2_name), inline=False)
        new_embed_2.add_field(name="Command to Bet", value='!bet '+team_2_name+' [number of tokens]', inline=False)
        await bet_msg_2.edit(embed=new_embed_2, content='')


    await channel.send('Updated bets')


async def check_open_bets(db, message):

    bets = db['bets']
    all_bets = bets.find()

    current_time = time.time()

    bet_ids_to_close = []

    for bet in all_bets:
        if (bet['open']) and ('timestamp' in bet) and bet['timestamp'] < current_time:
            bet_ids_to_close.append(bet['bet_id'])

    bets_closed = len(bet_ids_to_close)
    for bet_id_to_close in bet_ids_to_close:
        bets.update_one({'bet_id': bet_id_to_close}, {'$set': {'open': False}})

    result_message = 'Closed '+str(bets_closed)+' bets' if bets_closed > 0 else 'No bets were closed.'
    await message.channel.send(result_message)


    