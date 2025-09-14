

from safe_send import safe_send


async def ban_hero_handler(db, message, context):

    if context != 'OW':
        await safe_send(message.channel, 'The !ban command is only available in the Overwatch league.')
        return
    
    