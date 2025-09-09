
from safe_send import safe_add_field, safe_create_embed, safe_send_embed

async def help_drops_handler(message):

    help_embed = safe_create_embed('List of commands related to twitch drops:')
    
    safe_add_field(help_embed, '!drops', 'See how many twitch drops you have.', False)
    safe_add_field(help_embed, '!nextdrop', 'See how close you are to your next drop.', False)
    safe_add_field(help_embed, '!opendrop', 'Open a twitch drop for a prize. Make sure to use in the "opening drops" channel.', False)

    await safe_send_embed(message.channel, help_embed)