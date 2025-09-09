


from common_messages import invalid_number_of_params
from helpers import make_string_from_word_list, valid_number_of_params
from safe_send import safe_send
from shop import update_shop


async def set_item_price_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    
    item_id = int(params[1])

    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 2})

    if len(the_shop['offers']) < item_id:
        await safe_send(message.channel, 'There is no item in the shop with that id.')
        return
    
    new_item_price = int(params[2])
    actual_index = item_id - 1

    current_offer = the_shop['offers'][actual_index]
    current_offer['price'] = new_item_price
    the_shop['offers'][actual_index] = current_offer

    shop.update_one({"shop_id":2}, {"$set": {"offers": the_shop['offers']}})

    await update_shop(db, message)

    await safe_send(message.channel, 'Item price updated and shop updated.')

