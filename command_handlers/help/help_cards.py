import discord

async def help_cards_handler(message):

    help_embed = discord.Embed(title='List of cards commands:')
    help_embed.add_field(name='!cards', value='Shows a list of your cards.', inline=False)
    help_embed.add_field(name='!allcards', value='Get a link to a website that shows all of your cards at once.', inline=False)
    help_embed.add_field(name='!packs', value='Shows how many packs you own.', inline=False)
    help_embed.add_field(name='!openpack', value='Opens one of your card packs and gives you a card.', inline=False)
    help_embed.add_field(name='!viewcard [Card-ID]', value='Shows the image for any card.', inline=False)
    help_embed.add_field(name='!sellcard [Card-ID]', value='Sells any card for 20 tokens.', inline=False)
    help_embed.add_field(name='!sellallcards', value='Sells all your unlisted cards for 20 tokens each. Be carefuly, there is no confirmation message.', inline=False)
    help_embed.add_field(name='!givecard @Player [Card-ID]', value='Give a card to another user.', inline=False)
    help_embed.add_field(name='!listcard [Card-ID] [price]', value='Put your card for sale on the card market.', inline=False)
    help_embed.add_field(name='!unlistcard [Card-ID]', value='Take a card off sale of the card market.', inline=False)
    help_embed.add_field(name='!buycard [Card-ID]', value='Buy a card from the card market.', inline=False)
    help_embed.add_field(name='!cardmarket', value='Get a link to the card market website.', inline=False)
    help_embed.add_field(name='!gallery', value='Get a link to a gallery showing all of the SOL cards.', inline=False)
    help_embed.add_field(name='!cardsearch', value='Get a link to a webpage that helps you search for cards.', inline=False)
    help_embed.add_field(name='!totalpacks', value='See how many cards are still in packs.', inline=False)
    help_embed.add_field(name='!cardpage [number]', value="Get a link to a card's page on our website to see who owns each variant.", inline=False)
    help_embed.add_field(name='!cardbattle [card id] [battle type duel/capture/elimination] [min power] [max power]', value="Create a card battle with one of your cards to allow another player to challenge you!", inline=False)
    help_embed.add_field(name='!fightcard [opponent card id] [your card id]', value="Accept another player's card battle by fighting with a card of your own!", inline=False)
    help_embed.add_field(name='!top100', value="Show a list of the top 100 cards with the most power.", inline=False)

    await message.channel.send(embed=help_embed)