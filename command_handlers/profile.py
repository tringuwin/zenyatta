
from discord_actions import get_guild, get_member_by_username
from helpers import make_string_from_word_list
from user import get_fan_of, get_league_team, get_lvl_info, get_rival_of, get_user_gems, get_user_passes, get_user_pickaxes, get_user_tokens, user_exists
import constants




async def profile_handler(db, message, client):

    word_list = message.content.split()
    user = None
    if len(word_list) == 1:
        user = user_exists(db, message.author.id)
    else:
        username = make_string_from_word_list(word_list, 1)

        member = await get_member_by_username(client, username)
        if not member:
            await message.channel.send('There is no member with that username.')
            return
        
        user = user_exists(db, member.id)
    
    if not user:
        await message.channel.send('User not found.')
        return
    
    guild = await get_guild(client)

    level, xp = get_lvl_info(user)
    league_team = get_league_team(user)
    fan_of = get_fan_of(user)
    rival_of = get_rival_of(user)
    tokens = get_user_tokens(user)
    passes = get_user_passes(user)
    pickaxes = get_user_pickaxes(user)
    final_string = "**USER PROFILE FOR "+user['battle_tag']+':**\n'
    final_string += 'Level '+str(level)+' | XP: ('+str(xp)+'/'+str(level*100)+')\n'

    league_team_string = league_team
    if league_team in constants.EMOJI_TEAMS:
        team_emoji_id = constants.LEAGUE_TO_EMOJI_ID[league_team]
        team_emoji = guild.get_emoji(team_emoji_id)
        league_team_string = str(team_emoji)+' '+league_team_string

    fan_of_string = fan_of
    if fan_of in constants.EMOJI_TEAMS:
        fan_emoji_id = constants.LEAGUE_TO_EMOJI_ID[fan_of]
        fan_emoji = guild.get_emoji(fan_emoji_id)
        fan_of_string = str(fan_emoji)+' '+fan_of_string

    rival_of_string = rival_of
    if rival_of in constants.EMOJI_TEAMS:
        rival_emoji_id = constants.LEAGUE_TO_EMOJI_ID[rival_of]
        rival_emoji = guild.get_emoji(rival_emoji_id)
        rival_of_string = str(rival_emoji)+' '+rival_of_string
        
    final_string += 'League Team: **'+league_team_string+"**\n"
    final_string += 'Fan of Team: **'+fan_of_string+'**\n'
    final_string += 'Rival of Team: **'+rival_of_string+'**\n'

    final_string +='\n'
    final_string += '🪙 '+str(tokens)+' 🎟️ '+str(passes)+' ⛏️ '+str(pickaxes)+'\n'

    gems = get_user_gems(user)
    gem_line_1 = ''
    gem_line_2 = ''

    gem_index = 1
    for color, amount in gems.items():
        emoji_id = constants.COLOR_TO_EMOJI_ID[color]
        gem_emoji = guild.get_emoji(emoji_id)
        if gem_index < 6:
            gem_line_1 += str(gem_emoji)+' '+str(amount)+' '
        else:
            gem_line_2 += str(gem_emoji)+' '+str(amount)+' '
        gem_index +=1

    final_string +='\n'
    final_string += gem_line_1+'\n'+gem_line_2

    await message.channel.send(final_string)