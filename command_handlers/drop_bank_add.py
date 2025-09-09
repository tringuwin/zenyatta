
from helpers import get_constant_value, set_constant_value
from safe_send import safe_send


async def drop_bank_add_handler(db, message):

    val_to_add = float(message.content.split()[1])

    drop_bank_val = get_constant_value(db, 'drop_bank')

    drop_bank_val += val_to_add

    set_constant_value(db, 'drop_bank', drop_bank_val)

    await safe_send(message.channel, f"Drop bank value updated to {drop_bank_val}.")