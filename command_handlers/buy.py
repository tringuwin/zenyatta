
import time
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_role_by_id, give_role_to_user
from helpers import can_be_int, valid_number_of_params
from rewards import change_tokens
from shop import get_redemptions_channel, update_shop
from time_helpers import long_enough_for_shop, time_to_shop
from user import get_last_token_shop, get_user_tokens, user_exists
import constants


async def buy_handler(db, message, client):

    twitch_sub_role = await get_role_by_id(client, constants.TWITCH_SUB_ROLE)
    if not twitch_sub_role in message.author.roles:
        await message.reply('The Token Shop can only be used by Twitch Subscribers.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    raw_buy_item = params[1]
    if not can_be_int(raw_buy_item):
        await message.reply('Command not formatted correctly. Reference the Token Shop to see how to buy items.')
        return
    buy_item = int(raw_buy_item)

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 2})
    if buy_item < 1 or buy_item > len(the_shop['offers']):
        await message.reply('There is no item with that id.')
        return
    offer = the_shop['offers'][buy_item - 1]

    if offer['in_stock'] < 1:
        await message.reply('That item is not currently in stock.')
        return
    
    if buy_item != 7:
        last_token_shop = get_last_token_shop(user)
        long_enough, time_diff = long_enough_for_shop(last_token_shop)
        if not long_enough:
            time_left = time_to_shop(time_diff)
            await message.reply('You have used the Token Shop less than a week ago. You can use the shop again in **'+time_left+'**')
            return

    if offer['price'] > get_user_tokens(user):
        await message.reply('You do not have enough tokens to redeem this reward.')
        return

    offer['in_stock'] -= 1
    the_shop['offers'][buy_item-1] = offer
    shop.update_one({"shop_id":2}, {"$set": {"offers": the_shop['offers']}})

    await update_shop(db, message)
    await change_tokens(db, user, -1 * offer['price'], 'token-shop')
    if buy_item != 7:
        users = db['users']
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"last_token_shop": time.time()}})

    if offer['auto']:
    
        if buy_item == 7:
            pass
            # give player 500 poke-points
            # await change_pp(db, user, 500)
            # await message.reply('Success! You redeemed 500 PokePoints!')

    else:
        redemptions_channel = await get_redemptions_channel(message)
        final_string = 'Success! Your reward "'+offer['item_name']+'" has been redeemed. SpicyRagu will contact you soon to get you your reward!'
        final_string += '\n**It may take up to a week for you to be contacted. DO NOT PING/MESSAGE STAFF ABOUT REWARDS UNLESS IT HAS BEEN LONGER THAN 1 WEEK.**'
        final_string += '\n\nIf you would like to gift this reward to another user, please make a ticket in https://discord.com/channels/1130553449491210442/1202441473027477504 immediately.'
        await redemptions_channel.send('**User Redeemed Reward: '+offer['item_name']+'**\n'+'User ID: '+str(message.author.id)+'\nUser Name: '+message.author.display_name+'\nBattle Tag: '+user['battle_tag'])
        await message.reply(final_string)

    # send back confirm message