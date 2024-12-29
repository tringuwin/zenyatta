import time
import discord
import constants


async def feature_handler(message, client):
    
    feature = message.content[len("!feature "):].strip()

    feature_channel = client.get_channel(constants.FEATURE_CHANNEL)

    embed_msg = discord.Embed(
        title = "Upcoming Feature",
        description=feature
    )
    embed_msg.set_footer(text="Want this to be our priority? Cast your vote!")

    feature_msg = await feature_channel.send(embed=embed_msg)
    await feature_msg.add_reaction("✅")
    await feature_msg.add_reaction("❌")

    message_channel = message.channel
    await message_channel.send('Feature request sent.')