async def remove_passes_handler(db, message):
        users = db['users']
        all_users = users.find()
        users_affected = 0
        for user in all_users:
            if 'passes' in user and 'tokens' in user:
                num_passes = user['passes']
                if num_passes > 0:
                    tokens_to_give = num_passes * 10
                    new_tokens = user['tokens'] + tokens_to_give
                    users.update_one({'discord_id': user['discord_id']}, {'$set': {'tokens': new_tokens, 'passes': 0}})
                    users_affected += 1

        await message.channel.send(f'All users have had their passes removed and received 10 tokens for each pass they had. {users_affected} users were affected.')    