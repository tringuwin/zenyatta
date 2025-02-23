
import constants

async def top_100_handler(message):

    await message.channel.send(f'Check out the Top 100 cards with the most power on this web page!\n\n{constants.WEBSITE_DOMAIN}/sol/top-100-cards')