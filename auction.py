

from command_handlers.auction.end_auction import end_auction
from safe_send import safe_send
from time_helpers import get_current_day_est


async def check_auction(db, channel, client):

    auction_db = db['auction']
    auction_data = auction_db.find_one({'auction_id': 1})
    if not auction_data['is_open']:
        await safe_send(channel, 'Auction is not open.')
        return

    current_day = get_current_day_est()

    constants_db = db['constants']
    bid_day_obj = constants_db.find_one({'name': 'bid_day'})
    bid_day = bid_day_obj['value']

    if current_day == bid_day:
        await safe_send(channel, 'Bid day is still the current day.')
        return

    await safe_send(channel, 'Bid day is different than current day. Ending auction.')

    await end_auction(db, client)

    await safe_send(channel, 'Auction ended successfully.')
