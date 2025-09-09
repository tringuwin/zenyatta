import constants
from safe_send import safe_send

async def bracket_handler(message):

    await safe_send(message.channel, message.author.mention+f' Bracket for the current/next tournament:\n{constants.WEBSITE_DOMAIN}/bracket')