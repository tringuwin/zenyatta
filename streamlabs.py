import requests

stream_labs_data = 'https://streamlabs.com/api/v5/giveaway/history?token=B032D12F02A4ED3AA822&page=1'


async def check_streamlabs_raffles(db, channel):

    await channel.send('Checking for raffles.')
    
    redeem_req = requests.get(stream_labs_data)
    if redeem_req.status_code != 200:
        await channel.send('<@1112204092723441724> Error with streamlabs request.')
        return
    
    redeem_data = redeem_req.json()

    # 2024-05-26T21:57:57.000Z
    redeems = redeem_data['data']

    # sort only completed
    completed_redeems = []
    for redeem in redeems:
        if redeem['status'] == 'Completed':
            completed_redeems.append(redeem)

    print('Total number of redeems: '+str(len(completed_redeems)))


