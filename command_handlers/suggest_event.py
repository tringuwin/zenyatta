
import time
import discord
from discord_actions import is_dm_channel
import constants
from safe_send import safe_send, safe_send_embed, safe_set_footer

async def suggest_event_handler(message, client):
    
    event_idea = message.content[len("!suggestevent "):].strip()

    event_suggest_channel = client.get_channel(constants.SUGGEST_CHANNEL)

    embed_msg = discord.Embed(
        title = "Event Idea",
        description=event_idea
    )
    safe_set_footer(embed_msg, text="Suggest your own idea using the command !suggestevent [event idea here]")

    event_idea_msg = await safe_send_embed(event_suggest_channel, embed_msg)
    await event_idea_msg.add_reaction("👍")
    await event_idea_msg.add_reaction("👎")

    message_channel = message.channel
    bot_response = await safe_send(message_channel, 'Your event suggestion has been added!')
    if not is_dm_channel(message_channel):
        await message.delete()
        time.sleep(5)
        await bot_response.delete()