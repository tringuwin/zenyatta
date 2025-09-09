
from safe_send import safe_create_embed, safe_send_embed

async def help_drops_handler(message):

    help_embed = safe_create_embed('List of commands related to twitch drops:')
    help_embed.add_field(name='!drops', value='See how many twitch drops you have.', inline=False)
    help_embed.add_field(name='!nextdrop', value='See how close you are to your next drop.', inline=False)
    help_embed.add_field(name='!opendrop', value='Open a twitch drop for a prize. Make sure to use in the "opening drops" channel.', inline=False)

    await safe_send_embed(message.channel, help_embed)