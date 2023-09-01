
import discord

async def help_hanlder(message):

    help_embed = discord.Embed(title='List of commands:')
    help_embed.add_field(name='!battle BattleTagHere#1234', value='Register your battle tag with the SpicyRagu server', inline=False)
    help_embed.add_field(name='!helpteams', value='Show a list of commands related to making teams.', inline=False)
    help_embed.add_field(name='!events', value='Show a list of current server events', inline=False)
    help_embed.add_field(name='!join [event id]', value='Join an upcoming event', inline=False)
    help_embed.add_field(name='!suggestevent [idea here]', value='Suggest an idea for a future event', inline=False)
    help_embed.add_field(name='!tokens', value='See your current number of tokens', inline=False)
    help_embed.add_field(name='!passes', value='See your current passes', inline=False)
    help_embed.add_field(name='!sellpass', value='Sell 1 Priority Pass for 10 tokens', inline=False)
    help_embed.add_field(name='!gift', value='Earn a free gift every 8 hours!', inline=False)
    help_embed.add_field(name='!wager [number of tokens] [red, black, or green]', value='Use in the casino channel. Wager your tokens with European Roulette rules.', inline=False)
    help_embed.add_field(name='!funfact [fun fact here]', value='Add a fun fact about yourself that might be mentioned during livestreamed events', inline=False)
    help_embed.add_field(name='!hello', value='Say hi to the Zenyatta bot', inline=False)

    await message.channel.send(embed=help_embed)