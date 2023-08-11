

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
        await give_tokens(db, user, num)

        await message.channel.send('Tokens given')
    else:
        await message.channel.send('Could not find user with that ID')

async def change_passes(db, user, num):

    users = db['users']

    if "passes" in user:
        new_passes = user['passes'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": new_passes}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": num}})


async def give_passes_command(db, user_id, num, message):

    user = user_exists(db, int(user_id))

    if user:
        await change_passes(db, user, num)
        await message.channel.send('Passes given')
    else:
        await message.channel.send('Could not find user with that ID')


async def sell_pass_for_tokens(db, message):

    user = user_exists(db, int(message.author.id))

    if user_exists:

       if 'passes' in user and user['passes'] > 0:
           await change_passes(db, user, -1)
           await give_tokens(db, user, 10)
           await message.channel.send('You sold 1 Priority Pass for **10 Tokens!**')
       else:
           await message.channel.send('You do not have any priority passes to sell.')
        
           

    else:
        await message.channel.send('It looks like you are not registered yet. Please register first.')