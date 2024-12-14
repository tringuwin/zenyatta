import aiohttp
import time

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
        await message.channel.send('This command failed. Please let Spicy know.')
        return

    set_constant_value(db, 'raffle_status', 'ACTIVE') 
    await message.channel.send('500 Token Raffle Started on solnetwork')


async def end_raffle(db, message):

    raffle_status = get_constant_value(db, 'raffle_status')
    if raffle_status != 'ACTIVE':
        await message.channel.send('There is no raffle in progress. Please start it first with the command **!startraffle**')
        return
    
    # close
    close_error = False
    async with aiohttp.ClientSession() as session:
        async with session.put(
            'https://streamlabs.com/api/v5/giveaway/active/close?token=B032D12F02A4ED3AA822'
        ) as response:
            if response.status != 200:
                close_error = True
                print('close failed with code '+str(response.status))

    if close_error:
        await message.channel.send('This command failed. Please let Spicy know.')
        return
    
    time.sleep(1)

    # pick winner
    pick_error = False
    pick_result = None
    async with aiohttp.ClientSession() as session:
        async with session.post(
            'https://streamlabs.com/api/v5/giveaway/active/close?token=B032D12F02A4ED3AA822'
        ) as response:
            print('response is')
            print(response)
            if response.status != 200:
                pick_error = True
                print('pick failed with code '+str(response.status))

    if pick_error:
        await message.channel.send('This command failed. Please let Spicy know.')
        return
    print('pick result')
    print(pick_result)

    time.sleep(1)

    # complete
    complete_error = False
    async with aiohttp.ClientSession() as session:
        async with session.put(
            'https://streamlabs.com/api/v5/giveaway/active/complete?token=B032D12F02A4ED3AA822'
        ) as response:
            if response.status != 200:
                complete_error = True
                print('complete failed with code '+str(response.status))

    if complete_error:
        await message.channel.send('This command failed. Please let Spicy know.')
        return
    
    await message.channel.send('Raffle ended.')


    


    
