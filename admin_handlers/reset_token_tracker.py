

from helpers import get_constant_value, set_constant_value
from safe_send import safe_send


async def reset_token_tracker_handler(db, message):

    token_tracker = get_constant_value(db, 'token_tracker')

    for token_type in token_tracker:
        token_tracker[token_type] = {
            'total': 0,
            'given': 0,
            'taken': 0
        }

    set_constant_value(db, 'token_tracker', token_tracker)

    await safe_send(message.channel, 'Token tracker has been reset.')