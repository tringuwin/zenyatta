
twitch_token_url = 'https://id.twitch.tv/oauth2/authorize?client_id=46t2o4ora6yz8o1x5ws18qn2ueiz4v&redirect_uri=https://spicy-ragu-api-7d24f98c9e91.herokuapp.com/dva-webhook&response_type=code&scope=channel:manage:redemptions%20bits:read%20channel:read:subscriptions%20moderator:read:chatters%20channel:manage:predictions'
twitch_token_url_second = 'https://id.twitch.tv/oauth2/authorize?client_id=9ne2vin1hxd22nitknksqo0q9imwb1&redirect_uri=https://spicy-ragu-api-7d24f98c9e91.herokuapp.com/dva-webhook-2&response_type=code&scope=channel:manage:redemptions%20bits:read%20channel:read:subscriptions%20moderator:read:chatters%20channel:manage:predictions'

async def check_token_issue(db, channel):

    await channel.send('Checking for token issue.')
    
    constants_db = db['constants']
    token_issue_obj = constants_db.find_one({'name': 'token_issue'})
    token_issue_val = token_issue_obj['value']

    if token_issue_val['issue'] and ( not token_issue_val['notif'] ):
        await channel.send('We need a new twitch token: <@1112204092723441724>\n\n'+twitch_token_url)
        token_issue_val['notif'] = True
        constants_db.update_one({"name": 'token_issue'}, {"$set": {"value": token_issue_val}})


    token_issue_obj_2 = constants_db.find_one({'name': 'token_issue_second'})
    token_issue_val_2 = token_issue_obj_2['value']

    if token_issue_val_2['issue'] and ( not token_issue_val_2['notif'] ):
        await channel.send('We need a new second twitch token: <@1112204092723441724>\n\n'+twitch_token_url_second)
        token_issue_val_2['notif'] = True
        constants_db.update_one({"name": 'token_issue_second'}, {"$set": {"value": token_issue_val_2}})

