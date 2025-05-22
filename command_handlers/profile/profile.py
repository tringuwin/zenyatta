
from command_handlers.profile.make_rank_string.make_rank_string import make_rank_string
from command_handlers.profile.make_rivals_rank_string.make_rivals_rank_string import make_rivals_rank_string
from common_messages import not_registered_response
from discord_actions import get_guild
from helpers import generic_find_user, get_league_emoji_from_team_name, make_string_from_word_list
from user.user import get_fan_of, get_fan_of_rivals, get_fan_of_valorant, get_league_team_with_context, get_riot_id, get_rival_of, get_rival_of_rivals, get_rival_of_valorant, get_rivals_username, get_twitch_username, get_user_drop_boxes, get_user_gems, get_user_packs, get_user_pickaxes, get_user_ranks, get_user_rivals_rank, get_user_tokens, get_user_trophies, user_exists
import constants



async def overwatch_profile(message, client, user):
    
    if not 'battle_tag' in user:
        await message.channel.send('This is an Overwatch channel, I do not see an Overwatch battle tag in your profile.')
        return

    guild = await get_guild(client)

    league_team = get_league_team_with_context(user, 'OW')
    fan_of = get_fan_of(user)
    rival_of = get_rival_of(user)
    tokens = get_user_tokens(user)
    pickaxes = get_user_pickaxes(user)
    packs = get_user_packs(user)
    trophies = get_user_trophies(user)
    twitch_username = get_twitch_username(user)
    ranks = get_user_ranks(user)
    drops = get_user_drop_boxes(user)
    
    final_string = "**USER PROFILE FOR "+user['battle_tag']+':**\n'
    final_string += 'Twitch Username: **'+twitch_username+'**\n'
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
    drop_emoji_string = '<:spicy_drop:1327677388720701450>'
    final_string +='\n'
    final_string += '🪙 '+str(tokens)+' ⛏️ '+str(pickaxes)+' '+str(pack_emoji)+' '+str(packs)+' '+drop_emoji_string+' '+str(drops)+' 🏆 '+str(trophies)+'\n'

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

    await message.channel.send(final_string)



async def rivals_profile(message, client, user):

    if not 'rivals_username' in user:
        await message.channel.send('This is a Marvel Rivals channel, I do not see a Marvel Rivals username in your profile.')
        return

    guild = await get_guild(client)

    username = get_rivals_username(user)
    if username == '':
        username = '[Unknown Username]'

    league_team = get_league_team_with_context(user, 'MR')
    fan_of = get_fan_of_rivals(user)
    rival_of = get_rival_of_rivals(user)
    tokens = get_user_tokens(user)
    pickaxes = get_user_pickaxes(user)
    packs = get_user_packs(user)
    trophies = get_user_trophies(user)
    twitch_username = get_twitch_username(user)
    drops = get_user_drop_boxes(user)
    
    final_string = "**USER PROFILE FOR "+username+':**\n'
    final_string += 'Twitch Username: **'+twitch_username+'**\n'
    final_string += make_rivals_rank_string(user)+'\n\n'

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
    drop_emoji_string = '<:spicy_drop:1327677388720701450>'
    final_string +='\n'
    final_string += '🪙 '+str(tokens)+' ⛏️ '+str(pickaxes)+' '+str(pack_emoji)+' '+str(packs)+' '+drop_emoji_string+' '+str(drops)+' 🏆 '+str(trophies)+'\n'

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

    await message.channel.send(final_string)


async def valorant_profile(message, client, user):

    if not 'riot_id' in user:
        await message.channel.send('This is a Valorant channel, I do not see a Riot ID in your profile.')
        return

    guild = await get_guild(client)

    riot_id = get_riot_id(user)
    if riot_id == '':
        riot_id = '[Unknown Riot ID]'

    league_team = get_league_team_with_context(user, 'VL')
    fan_of = get_fan_of_valorant(user)
    rival_of = get_rival_of_valorant(user)
    tokens = get_user_tokens(user)
    pickaxes = get_user_pickaxes(user)
    packs = get_user_packs(user)
    trophies = get_user_trophies(user)
    twitch_username = get_twitch_username(user)
    drops = get_user_drop_boxes(user)
    
    final_string = "**USER PROFILE FOR "+riot_id+':**\n'
    final_string += 'Twitch Username: **'+twitch_username+'**\n\n'
    
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
    drop_emoji_string = '<:spicy_drop:1327677388720701450>'
    final_string +='\n'
    final_string += '🪙 '+str(tokens)+' ⛏️ '+str(pickaxes)+' '+str(pack_emoji)+' '+str(packs)+' '+drop_emoji_string+' '+str(drops)+' 🏆 '+str(trophies)+'\n'

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
    elif context == 'MR':
        await rivals_profile(message, client, user)
    elif context == 'VL':
        await valorant_profile(message, client, user)
    else:
        await message.channel.send('This command is not ready yet for this league.')