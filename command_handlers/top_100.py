
import constants
from safe_send import safe_send

async def top_100_handler(message):

    await safe_send(message.channel, f'Check out the Top 100 cards with the most power on this web page!\n\n{constants.WEBSITE_DOMAIN}/sol/top-100-cards')