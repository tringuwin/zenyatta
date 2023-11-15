
import discord

async def help_bonus_handler(message):
    
    help_embed = discord.Embed(title='List of bonus commands:')
    help_embed.add_field(name='!tokenleaderboard', value='See the top 10 users with the most tokens in the server.', inline=False)
    help_embed.add_field(name='!hello', value='Say hi to the Zenyatta bot', inline=False)
    help_embed.add_field(name='!gg ez', value='Zenyatta will respond with one of the classic "gg ez" responses.', inline=False)
    help_embed.add_field(name='!whichhero [question]', value='Ask the Zenyatta bot a question and it will respond with a hero. (Example: !whichhero should be nerfed?)', inline=False)

    await message.channel.send(embed=help_embed)
