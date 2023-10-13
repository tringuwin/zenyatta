
async def leaderboard_handler(db, message):
    
    users = db['users']
    all_users = users.find()

    filtered_users = [user for user in all_users if 'level' in user and 'xp' in user]

    sorted_users = sorted(filtered_users, key=lambda user: (user['level'], user['xp']), reverse=True)

    top_10_users = sorted_users[:10]

    final_string = '**SERVER LEVEL LEADERBOARD:**\n'
    for user in top_10_users:
        final_string += user['battle_tag']+'\n'

    await message.channel.send(final_string)
