import discord

from safe_send import safe_add_field, safe_create_embed, safe_send_embed

async def help_gems_handler(message):

    help_embed = safe_create_embed('List of gem commands:')

    safe_add_field(help_embed, '!gems', 'Show a list of your current gems. Also shows some information about gem values.', False)
    safe_add_field(help_embed, '!sellgems [color] [amount]', 'Sell gems of any color for 50 Tokens each.', False)
    safe_add_field(help_embed, '!donategems @user [color to give] [number]', 'Give gems to another user.', False)
    safe_add_field(help_embed, '!tradegem [color to give] @Partner [color to get]', 'Make a gem trade offer to another user.', False)
    safe_add_field(help_embed, '!denygemtrade', 'Deny a gem trade offer.', False)
    safe_add_field(help_embed, '!acceptgemtrade', 'Accept a gem trade offer.', False)
    safe_add_field(help_embed, '!tradegemset', 'Trade in a set of all 10 gem colors for 1,000 Tokens.', False)
    safe_add_field(help_embed, '!feedgem [card-id] [gem color]', 'Feed a gem to one of your cards to increase the power of the card.', False)

    await safe_send_embed(message.channel, help_embed)
