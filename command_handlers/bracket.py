import constants

async def bracket_handler(message):

    await message.channel.send(message.author.mention+f' Bracket for the current/next tournament:\n{constants.WEBSITE_DOMAIN}/bracket')