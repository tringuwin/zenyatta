

from command_handlers.twitch_api.raid_channel import raid_channel
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params

VALID_RAID_CHANNELS = [
    'main',
    'second',
    'third'
]

async def raid_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    from_channel = params[1].lowwer()
    to_channel = params[2].lower()

    if from_channel not in VALID_RAID_CHANNELS:
        await message.channel.send(f'Invalid raid channel: {from_channel}. Valid channels are: {", ".join(VALID_RAID_CHANNELS)}')
        return
    
    if to_channel not in VALID_RAID_CHANNELS:
        await message.channel.send(f'Invalid raid channel: {to_channel}. Valid channels are: {", ".join(VALID_RAID_CHANNELS)}')
        return
    
    await raid_channel(db, message, from_channel, to_channel)