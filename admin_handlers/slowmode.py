

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params


async def slowmode_handler(message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    slowmode_seconds = params[1]
    if not can_be_int(slowmode_seconds):
        await message.channel.send(f'Slowmode must be a number of seconds.')
        return
    
    slowmode_seconds = int(slowmode_seconds)

    await message.channel.edit(slowmode_delay=slowmode_seconds)

    await message.channel.send(f'Slowmode set to {slowmode_seconds} seconds.')