

from api import get_member
from discord_actions import get_guild

import constants
from rewards import change_tokens
from user.user import user_exists


async def end_auction(db, client):
    auction = db['auction']
    auction.update_one({"auction_id": 1}, {"$set": {'is_open': False}})
    data = auction.find_one({'auction_id': 1})

    guild = await get_guild(client)
    auction_channel = guild.get_channel(constants.DAILY_AUCTION_CHANNEL)
    redemptions_channel = guild.get_channel(constants.OFFER_REDEMPTIONS_CHANNEL_ID)

    won_string = 'No one bid on the item!'
    if data['highest_bidder_id'] != 0:

        player_mention = '[PLAYER NOT FOUND]'
        member = get_member(guild, data['highest_bidder_id'], 'End Auction')
        if member:
            player_mention = member.mention

        user_bid = data['highest_bid']

        won_string = player_mention+' won '+data['item_name']+' with a bid of '+str(user_bid)+' Tokens!'

        if member:
            user = user_exists(db, member.id)
            if user:
                await change_tokens(db, user, int(user_bid * -1), 'daily-auction')

    final_string = '--------------------------------\n'
    final_string += 'Auction Ended!\n'
    final_string += won_string
    
    await redemptions_channel.send(won_string)
    await auction_channel.send(final_string)


async def end_auction_handler(db, message, client):

    auction = db['auction']
    data = auction.find_one({'auction_id': 1})

    if not data['is_open']:
        await message.channel.send('There is no current auction.')
        return
    
    await end_auction(db, client)

    await message.channel.send('Auction ended.')