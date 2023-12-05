

from discord_actions import get_guild

import constants

async def end_auction_handler(db, message, client):

    auction = db['auction']
    data = auction.find_one({'auction_id': 1})

    if not data['is_open']:
        await message.channel.send('There is no current auction.')
        return
    
    auction.update_one({"auction_id": 1}, {"$set": {'is_open': False}})

    guild = await get_guild(client)
    auction_channel = guild.get_channel(constants.DAILY_AUCTION_CHANNEL)

    won_string = 'No one bid on the item!'
    if data['highest_bidder_id'] != 0:
        won_string = '[player name] won '+data['item_name']+' with a bid of '+str(data['highest_bid'])+' Tokens!'

    final_string = '--------------------------------\n'
    final_string += 'Auction Ended!\n'
    final_string += won_string
    
    await auction_channel.send(final_string)

    await message.channel.send('Auction ended.')