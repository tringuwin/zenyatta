
from safe_send import safe_create_embed, safe_send_embed, safe_add_field

async def help_handler(message):

    help_embed = safe_create_embed('List of commands:')

    safe_add_field(help_embed, '!battle BattleTagHere#1234', 'Register your battle tag with the Spicy Esports server', False)
    safe_add_field(help_embed, '!twitch TwitchUsernameHere', 'Add your twitch username to the server so you can be given rewards you earn on stream!', False)
    safe_add_field(help_embed, '!profile', 'Shows your profile for this Discord Server.', False)
    safe_add_field(help_embed, '!website', "Get a link to our community's official website.'", False)
    safe_add_field(help_embed, '!helpcasino', 'Show a list of commands related to the casino channels.', False)
    safe_add_field(help_embed, '!helpleague', 'Show a list of commands related to the Spicy Overwatch League.', False)
    safe_add_field(help_embed, '!helpgems', 'Show a list of commands related to gems.', False)
    safe_add_field(help_embed, '!helpbonus', 'Show a list of bonus commands.', False)
    safe_add_field(help_embed, '!helpcards', 'Show a list of card commands.', False)
    safe_add_field(help_embed, '!helpdrops', 'Show a list of commands related to twitch drops.', False)
    safe_add_field(help_embed, '!events', 'Show a list of current server events', False)
    safe_add_field(help_embed, '!bracket', 'Show the bracket for the next/current event.', False)
    safe_add_field(help_embed, '!join [event id]', 'Join an upcoming event', False)
    safe_add_field(help_embed, '!suggest [idea here]', 'Suggest an idea for this Discord server', False)
    safe_add_field(help_embed, '!tokens', 'See your current number of tokens', False)
    safe_add_field(help_embed, '!gift', 'Earn a free gift every 8 hours!', False)
    safe_add_field(help_embed, '!bid [number of tokens]', 'Bid on the current daily auction with your Tokens!', False)

    await safe_send_embed(message.channel, help_embed)