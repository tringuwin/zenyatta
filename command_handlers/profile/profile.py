

from common_messages import not_registered_response
from exceptions import CommandError
from helpers import generic_find_user, get_constant_value, get_league_emoji_from_team_name, make_string_from_word_list
from safe_send import safe_send
from user.user import get_fan_of_with_context, get_league_team_with_context, get_rival_of_with_context, get_twitch_username, get_user_drop_boxes, get_user_gems, get_user_packs, get_user_pickaxes, get_user_tokens, get_user_trophies, get_user_vouchers, user_exists
import constants


def get_team_display_string(team_name):

    if team_name == 'None':
        return 'None'

    team_emoji_string = get_league_emoji_from_team_name(team_name)
    return team_emoji_string+' '+team_name



def make_gem_string(user_gems):

    gem_line_1 = ''
    gem_line_2 = ''

    gem_index = 1
    for color, amount in user_gems.items():
        gem_emoji_string = constants.GEM_COLOR_TO_STRING[color]
        if gem_index < 6:
            gem_line_1 += gem_emoji_string+' '+str(amount)+' '
        else:
            gem_line_2 += gem_emoji_string+' '+str(amount)+' '
        gem_index +=1

    return gem_line_1+'\n'+gem_line_2



def get_voucher_estimated_value(db):

    return get_constant_value(db, 'spicy_price_in_usd')


def get_generic_profile_data(user, context, voucher_value):

    user_vouchers = get_user_vouchers(user)
    value_of_vouchers = user_vouchers * voucher_value

    return {
        'league_team': get_league_team_with_context(user, context),
        'fan_of': get_fan_of_with_context(user, context),
        'rival_of': get_rival_of_with_context(user, context),
        'tokens': get_user_tokens(user),
        'pickaxes': get_user_pickaxes(user),
        'packs': get_user_packs(user),
        'trophies': get_user_trophies(user),
        'vouchers': user_vouchers,
        'drops': get_user_drop_boxes(user),
        'gems': get_user_gems(user),
        'twitch_username': get_twitch_username(user),
        'value_of_vouchers': value_of_vouchers
    }


def get_league_team_string(league_team):

    team_string = get_team_display_string(league_team)
    return 'League Team: **'+team_string+"**\n"

def get_fan_of_string(fan_of):

    team_string = get_team_display_string(fan_of)
    return 'Fan of Team: **'+team_string+'**\n'

def get_rival_of_string(rival_of):

    team_string = get_team_display_string(rival_of)
    return 'Rival of Team: **'+team_string+'**\n'


def overwatch_profile(user, voucher_value):

    gen_data = get_generic_profile_data(user, 'OW', voucher_value)
 
    final_string = "**USER PROFILE FOR "+user['battle_tag']+':**\n'
    final_string += 'Twitch Username: **'+gen_data['twitch_username']+'**\n\n'
        
    final_string += get_league_team_string(gen_data['league_team'])
    final_string += get_fan_of_string(gen_data['fan_of'])
    final_string += get_rival_of_string(gen_data['rival_of'])

    final_string +='\n'
    vouchers_string =' '+constants.SPICY_VOUCHER_EMOJI_STRING+' '+str(gen_data['vouchers'])+' (Est. $'+str(round(gen_data['value_of_vouchers'],2))+')'
    final_string += '🪙 '+str(gen_data['tokens'])+' ⛏️ '+str(gen_data['pickaxes'])+' '+constants.SPICY_PACK_EMOJI_STRING+' '+str(gen_data['packs'])+' '+constants.SPICY_DROP_EMOJI_STRING+' '+str(gen_data['drops'])+' 🏆 '+str(gen_data['trophies'])+vouchers_string+'\n'

    final_string +='\n'
    final_string += make_gem_string(gen_data['gems'])

    return final_string


def rivals_profile(user, voucher_value):

    gen_data = get_generic_profile_data(user, 'MR', voucher_value)
    
    final_string = "**USER PROFILE FOR "+user['rivals_username']+':**\n'
    final_string += 'Twitch Username: **'+gen_data['twitch_username']+'**\n\n'

    final_string += get_league_team_string(gen_data['league_team'])
    final_string += get_fan_of_string(gen_data['fan_of'])
    final_string += get_rival_of_string(gen_data['rival_of'])

    final_string +='\n'
    vouchers_string =' '+constants.SPICY_VOUCHER_EMOJI_STRING+' '+str(gen_data['vouchers'])+' (Est. $'+str(round(gen_data['value_of_vouchers'],2))+')'
    final_string += '🪙 '+str(gen_data['tokens'])+' ⛏️ '+str(gen_data['pickaxes'])+' '+constants.SPICY_PACK_EMOJI_STRING+' '+str(gen_data['packs'])+' '+constants.SPICY_DROP_EMOJI_STRING+' '+str(gen_data['drops'])+' 🏆 '+str(gen_data['trophies'])+vouchers_string+'\n'

    final_string +='\n'
    final_string += make_gem_string(gen_data['gems'])

    return final_string


def valorant_profile(user, voucher_value):

    gen_data = get_generic_profile_data(user, 'VL', voucher_value)

    final_string = "**USER PROFILE FOR "+user['riot_id']+':**\n'
    final_string += 'Twitch Username: **'+gen_data['twitch_username']+'**\n'
    
    final_string += get_league_team_string(gen_data['league_team'])
    final_string += get_fan_of_string(gen_data['fan_of'])
    final_string += get_rival_of_string(gen_data['rival_of'])

    final_string +='\n'
    vouchers_string =' '+constants.SPICY_VOUCHER_EMOJI_STRING+' '+str(gen_data['vouchers'])+' (Est. $'+str(round(gen_data['value_of_vouchers'],2))+')'
    final_string += '🪙 '+str(gen_data['tokens'])+' ⛏️ '+str(gen_data['pickaxes'])+' '+constants.SPICY_PACK_EMOJI_STRING+' '+str(gen_data['packs'])+' '+constants.SPICY_DROP_EMOJI_STRING+' '+str(gen_data['drops'])+' 🏆 '+str(gen_data['trophies'])+vouchers_string+'\n'

    final_string +='\n'
    final_string += make_gem_string(gen_data['gems'])

    return final_string



def verify_overwatch_user(user):

    if not 'battle_tag' in user:
        raise CommandError('This is an Overwatch channel. I do not see an Overwatch battle tag in that profile.')


def verify_rivals_user(user):

    if not 'rivals_username' in user:
        raise CommandError('This is a Marvel Rivals channel. I do not see a Marvel Rivals username in that profile.')


def verify_valorant_user(user):

    if not 'riot_id' in user:
        raise CommandError('This is a Valorant channel. I do not see a Riot ID in that profile.')



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
        raise CommandError('User not found.')
    
    voucher_value = get_constant_value(db, 'spicy_price_in_usd')

    profile_string = ''
    if context == 'OW':
        verify_overwatch_user(user)
        profile_string = overwatch_profile(user, voucher_value)
    elif context == 'MR':
        verify_rivals_user(user)
        profile_string = rivals_profile(user, voucher_value)
    elif context == 'VL':
        verify_valorant_user(user)
        profile_string = valorant_profile(user, voucher_value)
    else:
        raise CommandError('This command is not ready yet for this league.')

    await safe_send(message.channel, profile_string)
