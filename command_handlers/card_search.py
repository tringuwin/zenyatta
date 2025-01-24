
import constants

async def card_search_handler(message):

    await message.channel.send(f'Use this web page to search for cards by player and season!\n\n{constants.WEBSITE_DOMAIN}/sol/card-search')