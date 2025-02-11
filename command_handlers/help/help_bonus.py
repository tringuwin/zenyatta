
import discord

async def help_bonus_handler(message):
    
    help_embed = discord.Embed(title='List of bonus commands:')
    help_embed.add_field(name='!donate [@user] [number of tokens]', value='Donate tokens to another user in this server!', inline=False)
    help_embed.add_field(name='!donatepass [@user]', value='Donate 1 Priority Pass another user in this server!', inline=False)
    help_embed.add_field(name='!sellpass', value='Sell 1 Priority Pass for 10 tokens', inline=False)
    help_embed.add_field(name='!sellpickaxe', value='Sell 1 Pickaxe for 15 tokens', inline=False)
    help_embed.add_field(name='!invitedby [@user]', value='Mention the user that invited you for you both to get the invite reward.', inline=False)
    help_embed.add_field(name='!leaguexp', value='Shows the XP Leaderboard for the monthly XP challenge.', inline=False)
    help_embed.add_field(name='!leaguexptotal', value='Shows the XP Leaderboard for the total XP teams have earned (since Season 3).', inline=False)
    help_embed.add_field(name='!store', value='Get a link to the official SOL Merch Store.', inline=False)
    help_embed.add_field(name='!rogue', value='Get a link to earn 20% off of Rogue Energy products and support our League!', inline=False)
    help_embed.add_field(name='!roguerank', value="See our server's rank among all Rogue Energy partners.", inline=False)
    help_embed.add_field(name='!auctiontimer', value='Shows how much time is left until the Daily Auction ends.', inline=False)
    help_embed.add_field(name='!leaderboard', value='Shows the Top 10 players by Level/XP and links to the full server leaderboard.', inline=False)
    help_embed.add_field(name='!tokenleaderboard', value='See the top 10 users with the most tokens in the server.', inline=False)
    help_embed.add_field(name='!hello', value='Say hi to the Zenyatta bot', inline=False)
    help_embed.add_field(name='!gg ez', value='Zenyatta will respond with one of the classic "gg ez" responses.', inline=False)
    help_embed.add_field(name='!whichhero [question]', value='Ask the Zenyatta bot a question and it will respond with a hero. (Example: !whichhero should be nerfed?)', inline=False)
    help_embed.add_field(name='!bandforband @user', value="Challenge another user to see who has the higher net worth!", inline=False)

    await message.channel.send(embed=help_embed)
