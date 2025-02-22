import discord

async def help_casino_handler(message):

    help_embed = discord.Embed(title='List of casino commands:')
    help_embed.add_field(name='!wager [number of tokens] [red, black, or green]', value='Use in the roulette channel. Wager your tokens with European Roulette rules.', inline=False)
    help_embed.add_field(name='!blackjack [number of tokens]', value='Use in the blackjack channel. Play simplified blackjack and win tokens if you beat the dealer!', inline=False)
    help_embed.add_field(name='!mine', value='Use in the mineshaft channel. Spend 20 tokens or a pickaxe to go mining and look for treasure!', inline=False)
    help_embed.add_field(name='!rps [number of tokens] [rock, paper, or scissors]', value='Play rock paper scissors with the Giselle bot and wager tokens!', inline=False)

    await message.channel.send(embed=help_embed)