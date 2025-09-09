

from command_handlers.xp_battle.battle_helpers import get_battle_constant_name
from helpers import get_constant_value, set_constant_value
from safe_send import safe_send


async def end_battle_handler(db, message, context):

    battle_constant_name = get_battle_constant_name(context)
    battle_info = get_constant_value(db, battle_constant_name)

    battle_info['battle_on'] = False
    battle_info['reg_open'] = False

    set_constant_value(db, battle_constant_name, battle_info)

    await safe_send(message.channel, 'Battle ended.')
