
import constants

async def website_handler(message):

    await message.channel.send(f'Check out the official SOL website here!\n\n{constants.WEBSITE_DOMAIN}/sol')