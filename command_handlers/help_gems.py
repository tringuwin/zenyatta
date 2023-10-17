import discord

async def help_gems_handler(message):

    help_embed = discord.Embed(title='List of gem commands:')
    help_embed.add_field(name='!gems', value='Show a list of your current gems. Also shows some information about gem values.', inline=False)
    help_embed.add_field(name='!sellgems [color] [amount]', value='Sell gems of any color for 50 Tokens each.', inline=False)
    help_embed.add_field(name='!tradegemset', value='Trade in a set of all 10 gem colors for 1,000 Tokens.', inline=False)

    await message.channel.send(embed=help_embed)
