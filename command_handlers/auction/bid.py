
from api import get_member
from command_handlers.auction.end_auction import end_auction
from common_messages import invalid_number_of_params, not_registered_response
from discord_actions import get_guild
from helpers import can_be_int, valid_number_of_params
from time_helpers import get_current_day_est
from user.user import get_user_tokens, user_exists

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
    
    cur_day = get_current_day_est()
    constants_db = db['constants']
    bid_day_obj = constants_db.find_one({'name': 'bid_day'})
    bid_day = bid_day_obj['value']
    if cur_day != bid_day:
        await end_auction(db, client)
        await message.channel.send('Sorry this auction has ended. There will be a new auction soon.')
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

    guild = await get_guild(client)
    auction_channel = guild.get_channel(constants.DAILY_AUCTION_CHANNEL)
    bot_channel = guild.get_channel(constants.BOT_CHANNEL)

    previous_bid_string = ''
    if data['highest_bidder_id'] != 0:
        previous_bidder_mention = '[PLAYER NOT FOUND]'
        previous_bidder = get_member(guild, data['highest_bidder_id'], 'Bid Handler')
        if previous_bidder:
            previous_bidder_mention = previous_bidder.mention
        previous_bid_string = '(Previous Bidder: '+previous_bidder_mention+')'

    auction.update_one({"auction_id": 1}, {"$set": 
        {
        'highest_bid': bid_amount,
        'highest_bidder_id': user['discord_id']
        }
    })

    final_string = '--------------------------------\n'
    final_string += message.author.mention+' bid **'+str(bid_amount)+' Tokens** on '+data['item_name']+' '+previous_bid_string+'\n'
    final_string += 'To bid on this item use the command **!bid [number of tokens]** in '+bot_channel.mention
    await auction_channel.send(final_string)
    
    await message.channel.send('You successfully bid '+str(bid_amount)+' Tokens on '+data['item_name']) 