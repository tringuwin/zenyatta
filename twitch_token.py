
from command_handlers.twitch_api.twitch_helpers import get_callback_url, get_client_id


# twitch_token_url = 'https://id.twitch.tv/oauth2/authorize?client_id=46t2o4ora6yz8o1x5ws18qn2ueiz4v&redirect_uri=https://spicy-ragu-api-7d24f98c9e91.herokuapp.com/dva-webhook&response_type=code&scope=channel:manage:redemptions%20bits:read%20channel:read:subscriptions%20moderator:read:chatters%20channel:manage:predictions'
# twitch_token_url_second = 'https://id.twitch.tv/oauth2/authorize?client_id=flqc4bwzq9w2i6bxyybbuxrjnxtn6g&redirect_uri=https://spicy-ragu-api-7d24f98c9e91.herokuapp.com/dva-webhook-2&response_type=code&scope=channel:manage:redemptions%20bits:read%20channel:read:subscriptions%20moderator:read:chatters%20channel:manage:predictions'



def create_token_url(channel_name):

    client_id = get_client_id(channel_name)
    callback_url = get_callback_url(channel_name)

    return f'https://id.twitch.tv/oauth2/authorize?client_id={client_id}&redirect_uri={callback_url}&response_type=code&scope=channel:manage:redemptions%20bits:read%20channel:read:subscriptions%20moderator:read:chatters%20channel:manage:predictions%20channel:edit:commercial%20channel:manage:raids'


async def check_token_issue(db, channel):

    await channel.send('Checking for token issue.')
    
    constants_db = db['constants']
    token_issue_obj = constants_db.find_one({'name': 'token_issue'})
    token_issue_val = token_issue_obj['value']

    if token_issue_val['issue'] and ( not token_issue_val['notif'] ):
        await channel.send('We need a new twitch token: <@1112204092723441724>\n\n'+create_token_url('main'))
        token_issue_val['notif'] = True
        constants_db.update_one({"name": 'token_issue'}, {"$set": {"value": token_issue_val}})


    token_issue_obj_2 = constants_db.find_one({'name': 'token_issue_second'})
    token_issue_val_2 = token_issue_obj_2['value']

    if token_issue_val_2['issue'] and ( not token_issue_val_2['notif'] ):
        await channel.send('We need a new second twitch token: <@1112204092723441724>\n\n'+create_token_url('second'))
        token_issue_val_2['notif'] = True
        constants_db.update_one({"name": 'token_issue_second'}, {"$set": {"value": token_issue_val_2}})


    token_issue_obj_3 = constants_db.find_one({'name': 'token_issue_third'})
    token_issue_val_3 = token_issue_obj_3['value']

    if token_issue_val_3['issue'] and ( not token_issue_val_3['notif'] ):
        await channel.send('We need a new third twitch token: <@1112204092723441724>\n\n'+create_token_url('third'))
        token_issue_val_3['notif'] = True
        constants_db.update_one({"name": 'token_issue_third'}, {"$set": {"value": token_issue_val_3}})