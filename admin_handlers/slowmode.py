

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
from safe_send import safe_send


async def slowmode_handler(message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    slowmode_seconds = params[1]
    if not can_be_int(slowmode_seconds):
        await safe_send(message.channel, f'Slowmode must be a number of seconds.')
        return
    
    slowmode_seconds = int(slowmode_seconds)

    if not (0 <= slowmode_seconds <= 21600):
        await safe_send(message.channel, 'Slowmode must be between 0 and 21600 seconds (6 hours).')
        return
    
    await message.channel.edit(slowmode_delay=slowmode_seconds)

    await safe_send(message.channel, f'Slowmode set to {slowmode_seconds} seconds.')