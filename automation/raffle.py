import aiohttp

from helpers import get_constant_value, set_constant_value

async def start_raffle(db, message):
    raffle_status = get_constant_value(db, 'raffle_status')
    if raffle_status != 'NONE':
        await message.channel.send('There is already a raffle in progress. Please end it first with the command **!endraffle**')
        return

    raffle_start_payload = {
        'platform': 'twitch'
    }


    request_error = False
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://streamlabs.com/api/v5/giveaway/start/3f166a7a-47c1-42b9-9ae3-de1cf280db5a?token=B032D12F02A4ED3AA822',
            json=raffle_start_payload
        ) as response:
            if response.status != 200:
                request_error = True
                print('failed with code '+str(response.status))


    if request_error:
        await message.channel.send('This command failed. Please let spicy ragu know.')
        return

    set_constant_value(db, 'raffle_status', 'ACTIVE') 
    await message.channel.send('500 Token Raffle Started on solnetwork')
