import discord

async def help_poke_handler(message):

    help_embed = discord.Embed(title='List of commands related to pokemon cards:')
    help_embed.add_field(name='!openpoke', value='Spend 100 PokePoints to open earn a real pokemon card!', inline=False)
    help_embed.add_field(name='!sellpoke [card id]', value='Sell a pokemon card for 20 Tokens', inline=False)
    help_embed.add_field(name='!viewpoke [card id]', value='View a pokemon card', inline=False)
    help_embed.add_field(name='!givepoke @user [card id]', value='Give one of your pokemon cards to another user', inline=False)
    help_embed.add_field(name='!allpokes', value='Get a link to a webpage that shows all of your Pokemon cards', inline=False)
    help_embed.add_field(name='!mypokes', value='See a list of pokemon card IDs that you own', inline=False)
    help_embed.add_field(name='!unopened', value='Get a link to a webpage that shows all Pokemon cards that have not been opened yet', inline=False)
    help_embed.add_field(name='!pokeleaderboard', value='See the leaderboard of users with the most unique Pokemon cards collected.', inline=False)
    help_embed.add_field(name='!address [address here]', value='ONLY USE THIS COMMAND IN DMS WITH THE BOT. Sets your shipping address where your card orders will be sent.', inline=False)
    help_embed.add_field(name='!order', value='See your current delivery order.', inline=False)
    help_embed.add_field(name='!addorder [card id]', value='Add a Pokemon Card you own to your card order.', inline=False)
    help_embed.add_field(name='!remorder [card id]', value='Remove a card in your current order.', inline=False)
    help_embed.add_field(name='!buyorder', value='Use PokePoints to buy your current order. Will cause a shipment of your selected Pokemon cards to the address you specified.', inline=False)

    await message.channel.send(embed=help_embed)