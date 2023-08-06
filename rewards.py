

async def give_tokens(db, user, num):

    users = db['users']
    
    if "tokens" in user:
        new_tokens = user['tokens'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": new_tokens}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": num}})

async def give_pass(db, user):

    users = db['users']

    if "passes" in user:
        new_passes = user['passes'] + 1
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": new_passes}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": 1}})