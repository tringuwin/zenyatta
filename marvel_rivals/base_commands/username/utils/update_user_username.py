
async def update_user_username(db, user, message, rivals_username):
    
    users = db['users']

    username_lower = rivals_username.lower()

    users.update_one({'discord_id': user['discord_id']}, {'$set': {'rivals_username_lower': username_lower, 'rivals_username': rivals_username}})

    await message.channel.send('Your Marvel Rivals username has been updated.')