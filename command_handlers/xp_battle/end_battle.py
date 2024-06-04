

from helpers import get_constant_value, set_constant_value


async def end_battle_handler(db, message):

    battle_info = get_constant_value(db, 'battle')

    battle_info['battle_on'] = False
    battle_info['reg_open'] = False

    set_constant_value(db, 'battle', battle_info)

    await message.channel.send('Battle ended.')
