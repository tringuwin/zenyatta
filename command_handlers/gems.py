
from common_messages import not_registered_response
from user import get_user_gems, user_exists
import constants


async def gems_handler(db, message, guild):
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    final_string = '**YOUR GEMS:**\n'

    user_gems = get_user_gems(user)
    for color, amount in user_gems.items():
        emoji_id = constants.COLOR_TO_EMOJI_ID[color]
        gem_emoji = guild.get_emoji(emoji_id)
        final_string += str(gem_emoji)+' '+color+': **'+str(amount)+'**\n'

    final_string += '--------------\n'
    final_string += 'Each gem is worth 50 Tokens seperately.\n'
    final_string += 'Or turn in a set of all 10 for 1,000 Tokens!'

    await message.channel.send(final_string)

