
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from shop import update_shop


async def set_stock_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        invalid_number_of_params(message)
        return
    
    raw_item_id = int(params[1])
    real_item_id = raw_item_id - 1

    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 2})

    the_shop['offers'][real_item_id]['in_stock'] = int(params[2])

    shop.update_one({"shop_id":2}, {"$set": {"offers": the_shop['offers']}})

    await update_shop(db, message)

    await message.channel.send('Stock of item has been changed and shop updated')
    