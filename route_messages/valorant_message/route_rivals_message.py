


from safe_send import safe_send
from valorant.base_commands.riot.riot import riot_handler


async def route_valorant_message(client, db, message, lower_message):

    if lower_message.startswith('!riot'):
        await riot_handler(db, message, client)

    else:
        await safe_send(message.channel, 'Invalid command. Please see **!help** for a list of commands.')