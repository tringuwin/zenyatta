import requests
from datetime import datetime

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

    print('Total number of completed redeems: '+str(len(completed_redeems)))

    constants_db = db['constants']
    last_redeems_obj = constants_db.find_one({'name': 'last_redeems'})
    last_redeem_val = last_redeems_obj['value']

    last_date = datetime.strptime(last_redeem_val, "%Y-%m-%dT%H:%M:%S.%fZ")

    valid_date_redeems = []

    for redeem in completed_redeems:

        redeem_date_raw = redeem['updated_at']
        redeem_date = datetime.strptime(redeem_date_raw, "%Y-%m-%dT%H:%M:%S.%fZ")

        if redeem_date > last_date:
            valid_date_redeems.append(redeem)

    print('Total number of valid date: '+str(len(valid_date_redeems)))




