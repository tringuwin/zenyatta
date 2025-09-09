import discord

from safe_send import safe_add_field, safe_create_embed, safe_send_embed

async def help_casino_handler(message):

    help_embed = safe_create_embed('List of casino commands:')
    
    safe_add_field(help_embed, '!wager [number of tokens] [red, black, or green]', 'Use in the roulette channel. Wager your tokens with European Roulette rules.', False)
    safe_add_field(help_embed, '!blackjack [number of tokens]', 'Use in the blackjack channel. Play simplified blackjack and win tokens if you beat the dealer!', False)
    safe_add_field(help_embed, '!mine', 'Use in the mineshaft channel. Spend 20 tokens or a pickaxe to go mining and look for treasure!', False)
    safe_add_field(help_embed, '!rps [number of tokens] [rock, paper, or scissors]', 'Play rock paper scissors with the Scovi bot and wager tokens!', False)

    await safe_send_embed(message.channel, help_embed)