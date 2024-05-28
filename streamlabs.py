import requests
from datetime import datetime

from rewards import change_tokens
from user import twitch_user_exists

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

    if len(valid_date_redeems) == 0:
        return

    most_recent_date_raw = None
    most_recent_date = None

    for valid_redeem in valid_date_redeems:
        
        redeem_date_raw = valid_redeem['updated_at']
        redeem_date = datetime.strptime(redeem_date_raw, "%Y-%m-%dT%H:%M:%S.%fZ")

        if (not most_recent_date ) or redeem_date > most_recent_date:
            most_recent_date_raw = redeem_date_raw
            most_recent_date = redeem_date

        winner_twitch = valid_redeem['winners'][0]['name']
        user = twitch_user_exists(db, winner_twitch)
        if not user:
            continue

        prize_name = valid_redeem['settings']['general']['name']

        # handle give prize
        if prize_name == '500 Tokens':
            print('Giving 500 tokens to '+winner_twitch)
            #change_tokens(db, user, 500)
        elif prize_name == 'SOL Card Pack':
            print('Giving a pack to '+winner_twitch)
        
        elif prize_name == 'Random Gem':
            print('Giving random gem to '+winner_twitch)

    constants_db.update_one({"name": 'last_redeems'}, {"$set": {"value": most_recent_date_raw}})

    print('Total number of valid date: '+str(len(valid_date_redeems)))




