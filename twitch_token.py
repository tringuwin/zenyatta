
async def check_token_issue(db, channel):

    await channel.send('Checking for token issue.')
    
    constants_db = db['constants']
    token_issue_obj = constants_db.find_one({'name': 'token_issue'})
    token_issue_val = token_issue_obj['value']

    if token_issue_val['issue'] and ( not token_issue_val['notif'] ):
        await channel.send('We need a new twitch token: <@1112204092723441724>')
        token_issue_val['notif'] = True
        constants_db.update_one({"name": 'token_issue'}, {"$set": {"value": token_issue_val}})

