import time
import discord
from discord_actions import is_dm_channel
import constants
from safe_send import safe_send, safe_send_embed, safe_set_footer

BLACK_LIST = [
    1291074955999580252,  # banz
    1247921202698260535, # lilac
    513207840878624776, # kaz
]

async def suggest_handler(message, client):
    
    if message.author.id in BLACK_LIST:
        await safe_send(message.channel, 'You are temporarily not allowed to use this command anymore due to abusing it.')
        return

    idea = message.content[len("!suggest "):].strip()
    if idea.lower().find('club') != -1:
        await safe_send(message.channel, 'Invalid suggestion.')
        return

    suggest_channel = client.get_channel(constants.SERVER_SUGGEST_CHANNEL)
    admin_channel = client.get_channel(constants.ADMIN_COMMAND_CHANNEL)

    embed_msg = discord.Embed(
        title = "Suggestion",
        description=idea
    )
    safe_set_footer(embed_msg, text="Suggest your own idea using the command !suggest [idea here]")

    idea_msg = await safe_send_embed(suggest_channel, embed_msg)
    await idea_msg.add_reaction("👍")
    await idea_msg.add_reaction("👎")

    message_channel = message.channel
    bot_response = await safe_send(message_channel, 'Your suggestion has been added!')
    await safe_send(admin_channel, 'Suggestion made by '+str(message.author.name)+'\n'+idea)
    if not is_dm_channel(message_channel):
        await message.delete()
        time.sleep(5)
        await bot_response.delete()