

from user import user_exists


async def give_tokens(db, user, num):

    print('giving '+str(num)+'tokens to user '+user['battle_tag'])
    users = db['users']
    
    if "tokens" in user:
        new_tokens = user['tokens'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": new_tokens}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": num}})


async def give_tokens_command(db, user_id, num, message):

    user = user_exists(db, int(user_id))

    if user:
        print('user exists')
        give_tokens(db, user, num)

        await message.channel.send('Tokens given')
    else:
        await message.channel.send('Could not find user with that ID')

async def give_pass(db, user):

    users = db['users']

    if "passes" in user:
        new_passes = user['passes'] + 1
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": new_passes}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": 1}})