
import discord

async def help_handler(message):

    help_embed = discord.Embed(title='List of commands:')
    help_embed.add_field(name='!battle BattleTagHere#1234', value='Register your battle tag with the Spicy OW server', inline=False)
    help_embed.add_field(name='!helpteams', value='Show a list of commands related to making teams.', inline=False)
    help_embed.add_field(name='!helpcasino', value='Show a list of commands related to the casino channels.', inline=False)
    help_embed.add_field(name='!helpleague', value='Show a list of commands related to the Spicy Overwatch League.', inline=False)
    help_embed.add_field(name='!helpgems', value='Show a list of commands related to gems.', inline=False)
    help_embed.add_field(name='!helpbonus', value='Show a list of bonus commands.', inline=False)
    help_embed.add_field(name='!events', value='Show a list of current server events', inline=False)
    help_embed.add_field(name='!bracket', value='Show the bracket for the next/current event.', inline=False)
    help_embed.add_field(name='!join [event id]', value='Join an upcoming event', inline=False)
    help_embed.add_field(name='!suggest [idea here]', value='Suggest an idea for this Discord server', inline=False)
    help_embed.add_field(name='!suggestevent [idea here]', value='Suggest an idea for a future event', inline=False)
    help_embed.add_field(name='!tokens', value='See your current number of tokens', inline=False)
    help_embed.add_field(name='!passes', value='See your current passes', inline=False)
    help_embed.add_field(name='!sellpass', value='Sell 1 Priority Pass for 10 tokens', inline=False)
    help_embed.add_field(name='!gift', value='Earn a free gift every 8 hours!', inline=False)
    help_embed.add_field(name='!bid [number of tokens]', value='Bid on the current daily auction with your Tokens!', inline=False)
    help_embed.add_field(name='!profile', value='Shows your profile for this Discord Server.', inline=False)
    help_embed.add_field(name='!leaderboard', value='Shows the Top 10 players by Level/XP and links to the full server leaderboard.', inline=False)
    help_embed.add_field(name='!donate [@user] [number of tokens]', value='Donate tokens to another user in this server!', inline=False)
    help_embed.add_field(name='!donatepass [@user]', value='Donate 1 Priority Pass another user in this server!', inline=False)
    help_embed.add_field(name='!invitedby [@user]', value='Mention the user that invited you for you both to get the invite reward.', inline=False)

    await message.channel.send(embed=help_embed)