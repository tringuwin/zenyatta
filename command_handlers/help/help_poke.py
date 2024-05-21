import discord

async def help_poke_handler(message):

    help_embed = discord.Embed(title='List of commands related to pokemon cards:')
    help_embed.add_field(name='!openpoke', value='Spend 100 PokePoints to open earn a real pokemon card!', inline=False)
    help_embed.add_field(name='!sellpoke [id]', value='Sell a pokemon card for 20 Tokens', inline=False)


    await message.channel.send(embed=help_embed)