

from marvel_rivals.base_commands.username.username import username_handler
from safe_send import safe_send


async def route_rivals_message(db, message, lower_message):

    if lower_message.startswith('!username'):
        await username_handler(db, message)

    else:
        await safe_send(message.channel, 'Invalid command. Please see **!help** for a list of commands.')