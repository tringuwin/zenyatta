
from helpers import get_constant_value, set_constant_value


async def drop_bank_add_handler(db, message):

    val_to_add = float(message.content.split()[1])

    drop_bank_val = get_constant_value(db, 'drop_bank')

    drop_bank_val += val_to_add

    set_constant_value(db, 'drop_bank', drop_bank_val)

    await message.channel.send(f"Drop bank value updated to {drop_bank_val}.")