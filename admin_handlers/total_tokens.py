from safe_send import safe_send


async def total_tokens_handler(db, message):
    
    users = db['users']
    all_users = users.find()

    total_tokens = 0
    for user in all_users:
        if 'tokens' in user:
            total_tokens += user['tokens']

    await safe_send(message.channel, 'Total tokens in circulation: '+str(total_tokens))
