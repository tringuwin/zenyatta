import time
import discord
import constants
from safe_send import safe_send, safe_send_embed, safe_set_footer


async def feature_handler(message, client):
    
    feature = message.content[len("!feature "):].strip()

    feature_channel = client.get_channel(constants.FEATURE_CHANNEL)

    embed_msg = discord.Embed(
        title = "Upcoming Feature",
        description=feature
    )
    safe_set_footer(embed_msg, text="Want this to be our priority? Cast your vote!")

    feature_msg = await safe_send_embed(feature_channel, embed_msg)
    await feature_msg.add_reaction("✅")
    await feature_msg.add_reaction("❌")

    message_channel = message.channel
    await safe_send(message_channel, 'Feature request sent.')