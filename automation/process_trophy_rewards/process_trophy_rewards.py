

from automation.process_trophy_rewards.utils.give_trophy_rewards import give_trophy_rewards
from helpers import get_constant_value, set_constant_value
import time

from safe_send import safe_send


def next_trophy_day(trophy_next_day):
    
    current_time = time.time()
    if current_time > trophy_next_day:
        return True
    
    return False


async def process_trophy_rewards(db, message):

    trophy_next_day = get_constant_value(db, 'trophy_next_day')

    if next_trophy_day(trophy_next_day):
        next_tropy_day_time = trophy_next_day + 86400
        set_constant_value(db, 'trophy_next_day', next_tropy_day_time)
        give_trophy_rewards(db)
        await safe_send(message.channel, 'Trophy rewards have been given.')
    else:
        await safe_send(message.channel, 'It has not been 24 hours since the last trophy reward was given.')