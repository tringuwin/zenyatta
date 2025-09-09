
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from shop import update_shop


async def delete_item_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 2)
    if valid_params:

        item_to_delete = int(params[1])
        item_to_delete_index = item_to_delete - 1

        shop = db['shop']
        the_shop = shop.find_one({'shop_id': 2})

        final_offers = []
        index = 0
        for offer in the_shop['offers']:
            if index != item_to_delete_index:
                final_offers.append(offer)
            index += 1

        shop.update_one({"shop_id":2}, {"$set": {"offers": final_offers}})

        await update_shop(db, message)

        await safe_send(message.channel, 'Item deleted and shop updated.')

    else:
        await invalid_number_of_params(message)