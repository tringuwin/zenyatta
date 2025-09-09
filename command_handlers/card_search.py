
import constants
from safe_send import safe_send

async def card_search_handler(message):

    await safe_send(message.channel, f'Use this web page to search for cards by player and season!\n\n{constants.WEBSITE_DOMAIN}/sol/card-search')