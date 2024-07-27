
import time

async def bump_lft_handler(db, message):

    lft_users = db['lft_users']

    lft_user = lft_users.find_one({'user_id': message.author.id})
    if not lft_user:
        await message.channel.send('It seems like you do not have an active LFT profile. Try the command **!helpLFT** for more info.')
        return
    
    # check if active
    if not lft_user['is_on']:
        await message.channel.send('Your LFT profile is not currently active. You can activate it with the command **!toggleLFT**')
        return

    # set bump time to now
    lft_users.update_one({'user_id': message.author.id}, {'$set': {'bump_time': time.time()}})

    # confirmation message
    await message.channel.send('Your LFT profile has been bumped to the top of the list!')