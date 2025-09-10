
import constants
from safe_send import safe_send

async def website_handler(message):

    await safe_send(message.channel, f'Check out the official SOL website here!\n\n{constants.WEBSITE_DOMAIN}/sol')