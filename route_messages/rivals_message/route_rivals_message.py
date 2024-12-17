

from api import send_msg
from marvel_rivals.base_commands.username import username_handler


async def route_rivals_message(db, message, lower_message):

    if lower_message.startswith('!username'):
        await username_handler(db, message)

    else:
        await send_msg(message.channel, 'Invalid command. Please see **!help** for a list of commands.', 'Invalid Command')