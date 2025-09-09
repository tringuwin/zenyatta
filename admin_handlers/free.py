

from safe_send import safe_send


async def free_handler(message):
    
    mentioned_users = message.mentions
    if not mentioned_users or len(mentioned_users) != 1:
        await safe_send(message.channel, 'Please mention exactly one user to free.')
        return
    
    user_to_free = mentioned_users[0]

    await user_to_free.edit(timed_out_until=None)

    await safe_send(message.channel, f'{user_to_free.name} has been freed from timeout!')