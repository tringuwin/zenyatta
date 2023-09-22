import time
import discord
from discord_actions import is_dm_channel
import constants

async def suggest_handler(message, client):
    
    event_idea = message.content[len("!suggest "):].strip()

    event_channel = client.get_channel(constants.SERVER_SUGGEST_CHANNEL)

    embed_msg = discord.Embed(
        title = "Suggestion From "+message.author.name,
        description=event_idea
    )
    embed_msg.set_footer(text="Suggest your own idea using the command !suggest [idea here]", icon_url=message.author.display_avatar)

    event_idea_msg = await event_channel.send(embed=embed_msg)
    await event_idea_msg.add_reaction("👍")

    message_channel = message.channel
    bot_response = await message_channel.send('Your suggestion has been added!')
    if not is_dm_channel(message_channel):
        await message.delete()
        time.sleep(5)
        await bot_response.delete()