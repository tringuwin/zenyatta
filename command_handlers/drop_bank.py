

from helpers import get_constant_value
from safe_send import safe_reply


async def drop_bank_handler(db, message):

    drop_bank_val = get_constant_value(db, 'drop_bank')

    await safe_reply(message, 'Drop Bank Balance: $'+str(drop_bank_val))