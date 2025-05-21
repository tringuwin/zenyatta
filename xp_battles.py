

from command_handlers.xp_battle.battle_helpers import get_battle_constant_name
from discord_actions import get_guild
from user.user import user_exists
import discord
import constants

async def contact_member_to_reg(member, client, context):

    default_message = 'Please register before entering XP Battles. To register, go to this channel ( https://discord.com/channels/1130553449491210442/1130553489106411591 ) and use this command to register: **!battle YourBattleTagHere#1234**'
    if context == 'MR':
        default_message = 'Please register before entering XP Battles. To register, go to this channel ( https://discord.com/channels/1130553449491210442/1318388766691295272 ) and use this command to register: **!username MarvelRivalsUsernameHere**'

    try:
        await member.send(default_message)
    except discord.Forbidden:
        guild = await get_guild(client)
        chat_channel = guild.get_channel(constants.CHAT_CHANNEL)
        await chat_channel.send(member.mention+' '+default_message+" (I tried to DM you but your privacy settings did not allow me to)")

def user_ready_for_battle(db, member, context):

    user = user_exists(db, member.id)
    if not user:
        return False
    
    if context == 'OW':
        if 'battle_tag' in user:
            return True
        
        return False

    elif context == 'MR':
        if 'rivals_username' in user:
            return True
        
        return False
    

    raise Exception('Invalid context for ready for battle')

async def add_to_battle(db, member, battle_info, client, context):

    if not battle_info['reg_open']:
        return
    
    sign_ups = battle_info['sign_ups']
    if member.id in sign_ups:
        return
    
    if not user_ready_for_battle(db, member, context):
        # not done
        await contact_member_to_reg(member, client, context)
        return
    
    battle_info['sign_ups'].append(member.id)
    constants_db = db['constants']
    battle_constant_name = get_battle_constant_name(context)
    constants_db.update_one({"name": battle_constant_name}, {"$set": {"value": battle_info}})

    
async def remove_from_battle(db, member, battle_info, battle_constant_name):

    if not battle_info['reg_open']:
        return
    
    sign_ups = battle_info['sign_ups']
    if not (member.id in sign_ups):
        return
    
    battle_info['sign_ups'].remove(member.id)
    constants_db = db['constants']
    constants_db.update_one({"name": battle_constant_name}, {"$set": {"value": battle_info}})


async def how_many_handler(db, message, context):

    constants_db = db['constants']
    battle_constant_name = get_battle_constant_name(context)
    battle_obj = constants_db.find_one({'name': battle_constant_name})
    battle_info = battle_obj['value']

    number_sign_ups = len(battle_info['sign_ups'])

    await message.channel.send('Total number of users signed up for the XP Battle: '+str(number_sign_ups))


def init_player_pools(battle_info):

    past_ref_players = []
    past_players = []
    valid_players = []

    for past_match in battle_info['past_players']:

        for past_user in past_match:
            if not (past_user in past_ref_players):
                past_ref_players.append(past_user)

    for user_id in battle_info['sign_ups']:
        if user_id in past_ref_players:
            past_players.append(user_id)
        else:
            valid_players.append(user_id)    

    return {
        'past_pool': past_players,
        'valid_pool': valid_players
    }

    