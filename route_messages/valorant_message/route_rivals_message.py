


from api import send_msg
from valorant.base_commands.riot.riot import riot_handler


async def route_valorant_message(db, message, lower_message):

    if lower_message.startswith('!riot'):
        await riot_handler(db, message)

    else:
        await send_msg(message.channel, 'Invalid command. Please see **!help** for a list of commands.', 'Invalid Command')