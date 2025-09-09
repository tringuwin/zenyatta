import discord

from safe_send import safe_add_field, safe_create_embed, safe_send_embed

async def help_cards_handler(message):

    help_embed = safe_create_embed('List of cards commands:')

    safe_add_field(help_embed, '!cards', 'Shows a list of your cards.', False)
    safe_add_field(help_embed, '!allcards', 'Get a link to a website that shows all of your cards at once.', False)
    safe_add_field(help_embed, '!packs', 'Shows how many packs you own.', False)
    safe_add_field(help_embed, '!openpack', 'Opens one of your card packs and gives you a card.', False)
    safe_add_field(help_embed, '!viewcard [Card-ID]', 'Shows the image for any card.', False)
    safe_add_field(help_embed, '!sellcard [Card-ID]', 'Sells any card for 20 tokens.', False)
    safe_add_field(help_embed, '!sellallcards', 'Sells all your unlisted cards for 20 tokens each. Be carefuly, there is no confirmation message.', False)
    safe_add_field(help_embed, '!givecard @Player [Card-ID]', 'Give a card to another user.', False)
    safe_add_field(help_embed, '!listcard [Card-ID] [price]', 'Put your card for sale on the card market.', False)
    safe_add_field(help_embed, '!unlistcard [Card-ID]', 'Take a card off sale of the card market.', False)
    safe_add_field(help_embed, '!buycard [Card-ID]', 'Buy a card from the card market.', False)
    safe_add_field(help_embed, '!cardmarket', 'Get a link to the card market website.', False)
    safe_add_field(help_embed, '!cardsearch', 'Get a link to a webpage that helps you search for cards.', False)
    safe_add_field(help_embed, '!totalcards', 'See the total number of cards you own.', False)
    safe_add_field(help_embed, '!totalpacks', 'See how many cards are still in packs.', False)
    safe_add_field(help_embed, '!cardpage [number]', "Get a link to a card's page on our website to see who owns each variant.", False)
    safe_add_field(help_embed, '!cardbattle [card id] [battle type duel/capture/elimination] [min power] [max power]', "Create a card battle with one of your cards to allow another player to challenge you!", False)
    safe_add_field(help_embed, '!fightcard [opponent card id] [your card id]', "Accept another player's card battle by fighting with a card of your own!", False)
    safe_add_field(help_embed, '!top100', "Show a list of the top 100 cards with the most power.", False)

    await safe_send_embed(message.channel, help_embed)