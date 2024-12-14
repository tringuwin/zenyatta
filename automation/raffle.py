import requests

from helpers import get_constant_value

async def start_raffle(db, message):

    raffle_status = get_constant_value(db, 'raffle_status')
    if raffle_status != 'NONE':
        await message.channel.send('There is already a raffle in progress. Please end it first with the command **!endraffle**')
        return
    
    raffle_start_payload = {
        'platform': 'twitch'
    }

    start_request = await requests.post('https://streamlabs.com/api/v5/giveaway/start/3f166a7a-47c1-42b9-9ae3-de1cf280db5a?token=B032D12F02A4ED3AA822', json=raffle_start_payload)

    print(start_request)

    await message.channel.send('500 Token Raffle Started on solnetwork')