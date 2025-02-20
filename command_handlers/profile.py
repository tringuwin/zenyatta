
from common_messages import not_registered_response
from discord_actions import get_guild, get_member_by_username
from helpers import generic_find_user, get_league_emoji_from_team_name, make_string_from_word_list
from poke_data import ALL_POKE_NUM
from user import get_fan_of, get_fan_of_rivals, get_league_team, get_lvl_info, get_rival_of, get_rival_of_rivals, get_rivals_league_team, get_rivals_username, get_twitch_username, get_user_drop_boxes, get_user_gems, get_user_packs, get_user_passes, get_user_pickaxes, get_user_poke_points, get_user_pokedex, get_user_ranks, get_user_tokens, get_user_trophies, user_exists
import constants


RANK_TEXT_TO_ID = {
    'Rank_Bronze Division_5': 'B5',
    'Rank_Bronze Division_4': 'B4',
    'Rank_Bronze Division_3': 'B3',
    'Rank_Bronze Division_2': 'B2',
    'Rank_Bronze Division_1': 'B1',

    'Rank_Silver Division_5': 'S5',
    'Rank_Silver Division_4': 'S4',
    'Rank_Silver Division_3': 'S3',
    'Rank_Silver Division_2': 'S2',
    'Rank_Silver Division_1': 'S1',

    'Rank_Gold Division_5': 'G5',
    'Rank_Gold Division_4': 'G4',
    'Rank_Gold Division_3': 'G3',
    'Rank_Gold Division_2': 'G2',
    'Rank_Gold Division_1': 'G1',

    'Rank_Platinum Division_5': 'P5',
    'Rank_Platinum Division_4': 'P4',
    'Rank_Platinum Division_3': 'P3',
    'Rank_Platinum Division_2': 'P2',
    'Rank_Platinum Division_1': 'P1',

    'Rank_Diamond Division_5': 'D5',
    'Rank_Diamond Division_4': 'D4',
    'Rank_Diamond Division_3': 'D3',
    'Rank_Diamond Division_2': 'D2',
    'Rank_Diamond Division_1': 'D1',

    'Rank_Master Division_5': 'M5',
    'Rank_Master Division_4': 'M4',
    'Rank_Master Division_3': 'M3',
    'Rank_Master Division_2': 'M2',
    'Rank_Master Division_1': 'M1',

    'Rank_GrandMaster Division_5': 'GM5',
    'Rank_GrandMaster Division_4': 'GM4',
    'Rank_GrandMaster Division_3': 'GM3',
    'Rank_GrandMaster Division_2': 'GM2',
    'Rank_GrandMaster Division_1': 'GM1',

    'Rank_Champ Division_5': 'C5',
    'Rank_Champ Division_4': 'C4',
    'Rank_Champ Division_3': 'C3',
    'Rank_Champ Division_2': 'C2',
    'Rank_Champ Division_1': 'C1',
}

def make_rank_string(ranks):

    tank = ranks['tank']
    tank_string = 'Tank: ?'
    if tank['tier'] != 'none':
        tank_string = 'Tank: '+RANK_TEXT_TO_ID[tank['tier']+' '+tank['div']]

    dps = ranks['offense']
    dps_string = 'DPS: ?'
    if dps['tier'] != 'none':
        dps_string = 'DPS: '+RANK_TEXT_TO_ID[dps['tier']+' '+dps['div']]

    sup = ranks['support']
    sup_string = 'Support: ?'
    if sup['tier'] != 'none':
        sup_string = 'Support: '+RANK_TEXT_TO_ID[sup['tier']+' '+sup['div']]

    return tank_string + ' | ' + dps_string + ' | ' + sup_string



async def overwatch_profile(message, client, user):
    
    guild = await get_guild(client)

    level, xp = get_lvl_info(user)
    league_team = get_league_team(user)
    fan_of = get_fan_of(user)
    rival_of = get_rival_of(user)
    tokens = get_user_tokens(user)
    passes = get_user_passes(user)
    pickaxes = get_user_pickaxes(user)
    packs = get_user_packs(user)
    #poke_points = get_user_poke_points(user)
    trophies = get_user_trophies(user)
    twitch_username = get_twitch_username(user)
    ranks = get_user_ranks(user)
    #pokedex = get_user_pokedex(user)
    drops = get_user_drop_boxes(user)
    
    final_string = "**USER PROFILE FOR "+user['battle_tag']+':**\n'
    final_string += 'Twitch Username: **'+twitch_username+'**\n'
    final_string += 'Level '+str(level)+' | XP: ('+str(xp)+'/'+str(level*100)+')\n'
    final_string += make_rank_string(ranks)+'\n\n'

    league_team_string = league_team
    if league_team in constants.EMOJI_TEAMS:
        team_emoji_string = get_league_emoji_from_team_name(league_team)
        league_team_string = team_emoji_string+' '+league_team_string

    fan_of_string = fan_of
    if fan_of in constants.EMOJI_TEAMS:
        fan_emoji_string = get_league_emoji_from_team_name(fan_of)
        fan_of_string = fan_emoji_string+' '+fan_of_string

    rival_of_string = rival_of
    if rival_of in constants.EMOJI_TEAMS:
        rival_emoji_string = get_league_emoji_from_team_name(rival_of)
        rival_of_string = rival_emoji_string+' '+rival_of_string
        
    final_string += 'League Team: **'+league_team_string+"**\n"
    final_string += 'Fan of Team: **'+fan_of_string+'**\n'
    final_string += 'Rival of Team: **'+rival_of_string+'**\n'

    pack_emoji = guild.get_emoji(constants.PACK_EMOJI_ID)
    #poke_emoji = guild.get_emoji(constants.POKE_EMOJI_ID)
    drop_emoji_string = '<:spicy_drop:1327677388720701450>'
    final_string +='\n'
    final_string += '🪙 '+str(tokens)+' 🎟️ '+str(passes)+' ⛏️ '+str(pickaxes)+' '+str(pack_emoji)+' '+str(packs)+' '+drop_emoji_string+' '+str(drops)+' 🏆 '+str(trophies)+'\n'

    gems = get_user_gems(user)
    gem_line_1 = ''
    gem_line_2 = ''

    gem_index = 1
    for color, amount in gems.items():
        gem_emoji_string = constants.GEM_COLOR_TO_STRING[color]
        if gem_index < 6:
            gem_line_1 += gem_emoji_string+' '+str(amount)+' '
        else:
            gem_line_2 += gem_emoji_string+' '+str(amount)+' '
        gem_index +=1

    final_string +='\n'
    final_string += gem_line_1+'\n'+gem_line_2

    #final_string += '\n\n<:spicedex:1242915011706228778> ' + str(pokedex) + '/' +str(ALL_POKE_NUM)

    await message.channel.send(final_string)



async def rivals_profile(message, client, user):

    guild = await get_guild(client)

    username = get_rivals_username(user)
    if username == '':
        username = '[Unknown Username]'

    level, xp = get_lvl_info(user)
    league_team = get_rivals_league_team(user)
    fan_of = get_fan_of_rivals(user)
    rival_of = get_rival_of_rivals(user)
    tokens = get_user_tokens(user)
    passes = get_user_passes(user)
    pickaxes = get_user_pickaxes(user)
    packs = get_user_packs(user)
    #poke_points = get_user_poke_points(user)
    trophies = get_user_trophies(user)
    twitch_username = get_twitch_username(user)
    #pokedex = get_user_pokedex(user)
    drops = get_user_drop_boxes(user)
    
    final_string = "**USER PROFILE FOR "+username+':**\n'
    final_string += 'Twitch Username: **'+twitch_username+'**\n'
    final_string += 'Level '+str(level)+' | XP: ('+str(xp)+'/'+str(level*100)+')\n\n'

    league_team_string = league_team
    if league_team in constants.EMOJI_TEAMS:
        team_emoji_string = get_league_emoji_from_team_name(league_team)
        league_team_string = team_emoji_string+' '+league_team_string

    fan_of_string = fan_of
    if fan_of in constants.EMOJI_TEAMS:
        fan_emoji_string = get_league_emoji_from_team_name(fan_of)
        fan_of_string = fan_emoji_string+' '+fan_of_string

    rival_of_string = rival_of
    if rival_of in constants.EMOJI_TEAMS:
        rival_emoji_string = get_league_emoji_from_team_name(rival_of)
        rival_of_string = rival_emoji_string+' '+rival_of_string
        
    final_string += 'League Team: **'+league_team_string+"**\n"
    final_string += 'Fan of Team: **'+fan_of_string+'**\n'
    final_string += 'Rival of Team: **'+rival_of_string+'**\n'

    pack_emoji = guild.get_emoji(constants.PACK_EMOJI_ID)
    #poke_emoji = guild.get_emoji(constants.POKE_EMOJI_ID)
    drop_emoji_string = '<:spicy_drop:1327677388720701450>'
    final_string +='\n'
    final_string += '🪙 '+str(tokens)+' 🎟️ '+str(passes)+' ⛏️ '+str(pickaxes)+' '+str(pack_emoji)+' '+str(packs)+' '+drop_emoji_string+' '+str(drops)+' 🏆 '+str(trophies)+'\n'

    gems = get_user_gems(user)
    gem_line_1 = ''
    gem_line_2 = ''

    gem_index = 1
    for color, amount in gems.items():
        gem_emoji_string = constants.GEM_COLOR_TO_STRING[color]
        if gem_index < 6:
            gem_line_1 += gem_emoji_string+' '+str(amount)+' '
        else:
            gem_line_2 += gem_emoji_string+' '+str(amount)+' '
        gem_index +=1

    final_string +='\n'
    final_string += gem_line_1+'\n'+gem_line_2

    #final_string += '\n\n<:spicedex:1242915011706228778> ' + str(pokedex) + '/' +str(ALL_POKE_NUM)

    await message.channel.send(final_string)



async def profile_handler(db, message, client, context):

    word_list = message.content.split()
    user = None
    not_reg = False
    if len(word_list) == 1:
        user = user_exists(db, message.author.id)
        if not user:
            not_reg = True
    else:
        username = make_string_from_word_list(word_list, 1)
        user = await generic_find_user(client, db, username)
    
    if not_reg:
        await not_registered_response(message, context)
        return

    if not user:
        await message.channel.send('User not found.')
        return

    if context == 'OW':
        await overwatch_profile(message, client, user)
    else:
        await rivals_profile(message, client, user)