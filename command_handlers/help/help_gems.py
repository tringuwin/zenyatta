import discord

from safe_send import safe_send_embed

async def help_gems_handler(message):

    help_embed = discord.Embed(title='List of gem commands:')
    help_embed.add_field(name='!gems', value='Show a list of your current gems. Also shows some information about gem values.', inline=False)
    help_embed.add_field(name='!sellgems [color] [amount]', value='Sell gems of any color for 50 Tokens each.', inline=False)
    help_embed.add_field(name='!donategems @user [color to give] [number]', value='Give gems to another user.', inline=False)
    help_embed.add_field(name='!tradegem [color to give] @Partner [color to get]', value='Make a gem trade offer to another user.', inline=False)
    help_embed.add_field(name='!denygemtrade', value='Deny a gem trade offer.', inline=False)
    help_embed.add_field(name='!acceptgemtrade', value='Accept a gem trade offer.', inline=False)
    help_embed.add_field(name='!tradegemset', value='Trade in a set of all 10 gem colors for 1,000 Tokens.', inline=False)
    help_embed.add_field(name='!feedgem [card-id] [gem color]', value='Feed a gem to one of your cards to increase the power of the card.', inline=False)

    await safe_send_embed(message.channel, help_embed)
