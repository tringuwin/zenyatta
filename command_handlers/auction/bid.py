
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
from user import get_user_tokens, user_exists

import constants

async def bid_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    auction = db['auction']
    data = auction.find_one({'auction_id': 1})
    if not data['is_open']:
        await message.channel.send('There is no daily auction open at the moment.')
        return
    
    bid_amount = params[1]
    if not can_be_int(bid_amount):
        await message.channel.send(bid_amount+' is not a number.')
        return
    
    bid_amount = int(bid_amount)
    current_bid = data['highest_bid']
    if bid_amount <= current_bid:
        await message.channel.send(str(bid_amount)+' is not higher than the current bid of '+str(current_bid)+' Tokens.')
        return

    user_tokens = get_user_tokens(user)
    if user_tokens < bid_amount:
        await message.channel.send('You do not have enough tokens for that bid.')
        return
    
    auction.update_one({"auction_id": 1}, {"$set": 
        {
        'highest_bid': bid_amount,
        'highest_bidden_id': user['discord_id']
        }
    })

    guild = await get_guild(client)
    auction_channel = guild.get_channel(constants.DAILY_AUCTION_CHANNEL)
    bot_channel = guild.get_channel(constants.BOT_CHANNEL)

    final_string = '[player name] bid **'+str(bid_amount)+' Tokens** on '+data['item_name']+'(Previous Bidder: [player name])\n'
    final_string += 'To bid on this item use the command **!bid [number of tokens]** in '+bot_channel.mention +'\n'
    final_string += '--------------------------------'

    await auction_channel.send(final_string)
    
    await message.channel.send('You successfully bid '+str(bid_amount)+' Tokens on '+data['item_name']) 