
from api import send_msg
from command_handlers.address import address_handler


async def route_dm_message(db, message):

    if message.content.lower().startswith('!address '):
        await address_handler(db, message)
       
    else:
        await send_msg(message.channel, 'Sorry, I do not respond to messages in Direct Messages. Please only use commands in the #bot-commands channel of the Spicy Esports Discord server.', 'DM Alert')