
from discord_actions import get_guild, get_member_by_username
from helpers import make_string_from_word_list
from user import get_league_team, get_lvl_info, get_user_gems, get_user_passes, get_user_pickaxes, get_user_tokens, user_exists
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
    

    level, xp = get_lvl_info(user)
    league_team = get_league_team(user)
    tokens = get_user_tokens(user)
    passes = get_user_passes(user)
    pickaxes = get_user_pickaxes(user)
    final_string = "**USER PROFILE FOR "+user['battle_tag']+':**\n'
    final_string += 'Level '+str(level)+' | XP: ('+str(xp)+'/'+str(level*100)+')\n'
    final_string += 'League Team: **'+league_team+"**\n"
    final_string += '🪙 '+str(tokens)+' 🎟️ '+str(passes)+' ⛏️ '+str(pickaxes)+'\n'
    final_string +='\n'


    gems = get_user_gems(user)
    gem_line_1 = ''
    gem_line_2 = ''

    guild = await get_guild(client)
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