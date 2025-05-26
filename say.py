from api import send_msg
from discord_actions import get_guild
import constants

async def say_handler(message, client):
    rest = message.content[len("!say "):].strip()
    guild = await get_guild(client)
    chat_channel = guild.get_channel(constants.CHAT_CHANNEL)
    await send_msg(chat_channel, rest, '!say')