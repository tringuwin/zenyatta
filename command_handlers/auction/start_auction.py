

from common_messages import invalid_number_of_params
from discord_actions import get_guild
from helpers import make_string_from_word_list

import constants

async def start_auction_handler(db, message, client):

    word_parts = message.content.split()
    if len(word_parts) < 2:
        await invalid_number_of_params(message)
        return

    auction = db['auction']
    data = auction.find_one({'auction_id': 1})

    if data['is_open']:
        await message.channel.send('An auction is currentl open. Please end the current auction first.')
        return
    
    item_name = make_string_from_word_list(word_parts, 1)
    

    auction.update_one({"auction_id": 1}, {"$set": 
        {
        'item_name': item_name,
        'is_open': True,
        'highest_bid': 10,
        'highest_bidden_id': 0
        }
    })

    guild = await get_guild(client)
    auction_channel = guild.get_channel(constants.DAILY_AUCTION_CHANNEL)
    bot_channel = guild.get_channel(constants.BOT_CHANNEL)

    final_string = 'NEW AUCTION STARTED FOR: **'+item_name+'**\n'
    final_string += 'Starting bid is **10 Tokens**\n'
    final_string += 'To bid on this item use the command **!bid [number of tokens]** in '+bot_channel.mention +'\n'
    final_string += '--------------------------------'

    await auction_channel.send(final_string)

    await message.channel.send('Auction started.')
    

