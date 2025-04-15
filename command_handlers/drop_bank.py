

from helpers import get_constant_value


async def drop_bank_handler(db, message):

    drop_bank_val = get_constant_value(db, 'drop_bank')

    await message.reply('Drop Bank Balance: '+str(drop_bank_val))