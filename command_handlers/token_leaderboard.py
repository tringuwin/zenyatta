
async def token_leaderboard_handler(db, message):
    
    users = db['users']
    all_users = users.find()

    filtered_users = [user for user in all_users if 'tokens' in user]

    sorted_users = sorted(filtered_users, key=lambda x: x["tokens"], reverse=True)

    top_10_users = sorted_users[:10]

    final_string = '**SERVER TOKEN LEADERBOARD:**\n'
    user_index = 1
    for user in top_10_users:

        user_tag = user['battle_tag']
        first_part = user_tag.split('#')[0]

        final_string += "**"+str(user_index)+".** "+first_part
        final_string += ' | Tokens: '+str(user['tokens'])+'\n'
        user_index += 1

    await message.channel.send(final_string)