
from common_messages import not_registered_response
from user import get_user_gems, user_exists

color_to_emoji_id = {
    'red': 1159202371998597211,
    'blue': 1159202447676424292,
    'yellow': 1159202451652624495,
    'green': 1159202443947679885,
    'purple': 1159202449068916837,
    'orange': 1159202446128730153,
    'teal': 1159202442559361104,
    'pink': 1159202453028360334,
    'white': 1159202441116516362,
    'black': 1159202439031959643
}

async def gems_handler(db, message, guild):
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    final_string = '**YOUR GEMS:**\n'

    user_gems = get_user_gems(user)
    for color, amount in user_gems.items():
        emoji_id = color_to_emoji_id[color]
        gem_emoji = guild.get_emoji(emoji_id)
        final_string += str(gem_emoji)+' '+color+': **'+str(amount)+'**\n'

    await message.channel.send(final_string)

