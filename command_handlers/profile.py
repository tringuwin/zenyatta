
from discord_actions import get_member_by_username
from helpers import make_string_from_word_list
from user import get_league_team, get_lvl_info, get_user_passes, get_user_pickaxes, get_user_tokens, user_exists


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

    await message.channel.send(final_string)