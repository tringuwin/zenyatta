
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int
from rewards import change_tokens
from user import get_user_gems, user_exists
import constants


async def sell_gems_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    word_parts = message.content.split()
    if len(word_parts) != 2 and len(word_parts) != 3:
        await invalid_number_of_params(message)
        return
    
    color_to_sell = word_parts[1].lower()

    if not color_to_sell in constants.DEFAULT_GEMS:
        await message.channel.send(color_to_sell+' is not a valid gem color.')
        return 

    num_to_sell = 1
    if len(word_parts) == 3:
        num_to_sell_string = word_parts[2]
        if not can_be_int(num_to_sell_string):
            await message.channel.send('Please enter a number of gems to sell like: **!sellgem red 3**')
            return 
        num_to_sell = int(num_to_sell_string)

    if num_to_sell < 1:
        await message.channel.send('You need to specify a postive number of gems to sell. (Duh)')
        return
    
    users_gems = get_user_gems(user)
    number_of_gem_color = users_gems[color_to_sell]
    if number_of_gem_color < num_to_sell:
        await message.channel.send('You do not have enough of this color gem for this sale.')
        return
    
    tokens_to_give = num_to_sell * 50
    users_gems[color_to_sell] -= num_to_sell

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {'gems': users_gems}})
    await change_tokens(db, user, tokens_to_give)

    await message.channel.send('Success! You sold '+str(num_to_sell)+' '+color_to_sell+' gems for '+str(tokens_to_give)+' Tokens!')

    