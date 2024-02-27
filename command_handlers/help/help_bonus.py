
import discord

async def help_bonus_handler(message):
    
    help_embed = discord.Embed(title='List of bonus commands:')
    help_embed.add_field(name='!auctiontimer', value='Shows how much time is left until the Daily Auction ends.', inline=False)
    help_embed.add_field(name='!subtimer', value='Shows how many days are left for your Twitch Sub Lootbox (if you are a Twitch Sub).', inline=False)
    help_embed.add_field(name='!leaderboard', value='Shows the Top 10 players by Level/XP and links to the full server leaderboard.', inline=False)
    help_embed.add_field(name='!tokenleaderboard', value='See the top 10 users with the most tokens in the server.', inline=False)
    help_embed.add_field(name='!hello', value='Say hi to the Zenyatta bot', inline=False)
    help_embed.add_field(name='!gg ez', value='Zenyatta will respond with one of the classic "gg ez" responses.', inline=False)
    help_embed.add_field(name='!whichhero [question]', value='Ask the Zenyatta bot a question and it will respond with a hero. (Example: !whichhero should be nerfed?)', inline=False)
    help_embed.add_field(name='!spicyowrank', value="See this Discord server's rank compared to all Overwatch Themed Discord servers.", inline=False)

    await message.channel.send(embed=help_embed)
