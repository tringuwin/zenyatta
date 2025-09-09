
from command_handlers.xp_battle.battle_helpers import get_battle_constant_name, get_battle_game_name, get_default_game_teams
from discord_actions import get_guild
import constants
from helpers import set_constant_value
from safe_send import safe_send


async def start_battle_handler(db, message, client, context):

    constants_db = db['constants']
    battle_constant_name = get_battle_constant_name(context)
    battle_obj = constants_db.find_one({'name': battle_constant_name})
    battle_info = battle_obj['value']

    if battle_info['battle_on']:
        await safe_send(message.channel, 'There is already an XP Battle in progress. Please end that one first.')
        return
    
    guild = await get_guild(client)
    xp_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)

    game_name = get_battle_game_name(context)
    xp_message = await safe_send(xp_channel, 'A NEW '+game_name+' XP BATTLE IS STARTING NOW! REACT WITH ⚔️ FOR A CHANCE TO JOIN!')
    await xp_message.add_reaction('⚔️')
    
    battle_info['battle_on'] = True
    battle_info['reg_open'] = True
    battle_info['reg_message_id'] = xp_message.id
    battle_info['sign_ups'] = []
    battle_info['current_players'] = []
    battle_info['current_teams'] = get_default_game_teams(context)
    constants_db.update_one({"name": battle_constant_name}, {"$set": {"value": battle_info}})
    set_constant_value(db, 'battle_context', context)

    await safe_send(message.channel, 'Battle Sign-Up Started')