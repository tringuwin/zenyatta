
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from rewards import change_passes, change_tokens
from shop import get_redemptions_channel
from user import get_user_tokens, user_exists
import constants


async def buy_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    raw_buy_item = params[1]
    if not can_be_int(raw_buy_item):
        await message.channel.send('Command not formatted correctly. Reference the Token Shop to see how to buy items.')
        return
    buy_item = int(raw_buy_item)

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 1})
    if buy_item < 1 or buy_item > len(the_shop['offers']):
        await message.channel.send('There is no item with that id.')
        return
    offer = the_shop['offers'][buy_item - 1]

    if offer['in_stock'] < 1:
        await message.channel.send('That item is not currently in stock.')
        return

    if offer['price'] > get_user_tokens(user):
        await message.channel.send('You do not have enough tokens to redeem this reward.')
        return

    await change_tokens(db, user, -1 * offer['price'])
    if offer['auto']:
    
        if buy_item == 5:
            # give player 1 priority pass
            change_passes(db, user, 1)
            await message.channel.send('Success! You redeemed a priority pass!')

    else:
        redemptions_channel = await get_redemptions_channel(message)
        await redemptions_channel.send('**User Redeemed Reward: '+offer['item_name']+'**\n'+'User ID: '+str(message.author.id)+'\nUser Name: '+message.author.display_name)
        await message.channel.send('Success! Your reward "'+offer['item_name']+'" has been redeemed. SpicyRagu will contact you soon to get you your reward!')

    # send back confirm message