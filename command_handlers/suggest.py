import time
import discord
from discord_actions import is_dm_channel
import constants

BLACK_LIST = [
    1291074955999580252  # banz
]

async def suggest_handler(message, client):
    
    if message.author.id in BLACK_LIST:
        await message.channel.send('You are temporarily not allowed to use this command anymore due to abusing it.')
        return

    idea = message.content[len("!suggest "):].strip()
    if idea.lower().find('club') != -1:
        await message.channel.send('Invalid suggestion.')
        return

    suggest_channel = client.get_channel(constants.SERVER_SUGGEST_CHANNEL)
    admin_channel = client.get_channel(constants.ADMIN_COMMAND_CHANNEL)

    embed_msg = discord.Embed(
        title = "Suggestion",
        description=idea
    )
    embed_msg.set_footer(text="Suggest your own idea using the command !suggest [idea here]")

    idea_msg = await suggest_channel.send(embed=embed_msg)
    await idea_msg.add_reaction("👍")
    await idea_msg.add_reaction("👎")

    message_channel = message.channel
    bot_response = await message_channel.send('Your suggestion has been added!')
    await admin_channel.send('Suggestion made by '+str(message.author.name)+'\n'+idea)
    if not is_dm_channel(message_channel):
        await message.delete()
        time.sleep(5)
        await bot_response.delete()