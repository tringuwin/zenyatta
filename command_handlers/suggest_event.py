
import time
import discord
from discord_actions import is_dm_channel
import constants

async def suggest_event_handler(message, client):
    
    event_idea = message.content[len("!suggestevent "):].strip()

    event_suggest_channel = client.get_channel(constants.SUGGEST_CHANNEL)

    embed_msg = discord.Embed(
        title = "Event Idea",
        description=event_idea
    )
    embed_msg.set_footer(text="Suggest your own idea using the command !suggestevent [event idea here]")

    event_idea_msg = await event_suggest_channel.send(embed=embed_msg)
    await event_idea_msg.add_reaction("👍")

    message_channel = message.channel
    bot_response = await message_channel.send('Your event suggestion has been added!')
    if not is_dm_channel(message_channel):
        await message.delete()
        time.sleep(5)
        await bot_response.delete()