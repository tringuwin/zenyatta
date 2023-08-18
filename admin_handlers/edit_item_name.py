
from common_messages import invalid_number_of_params
from helpers import make_string_from_word_list
from shop import update_shop


async def edit_item_name_handler(db, message):

    word_parts = message.content.split(' ')
    if len(word_parts) < 3:
        await invalid_number_of_params(message)
        return
    
    item_id = int(word_parts[1])

    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 1})

    if len(the_shop['offers']) < item_id:
        await message.channel.send('There is no item in the shop with that id.')
        return
    
    new_item_name = make_string_from_word_list(word_parts, 2)
    actual_index = item_id - 1

    current_offer = the_shop['offers'][actual_index]
    current_offer['item_name'] = new_item_name
    the_shop['offers'][actual_index] = current_offer

    shop.update_one({"shop_id":1}, {"$set": {"offers": the_shop['offers']}})

    await update_shop(db, message)

    await message.channel.send('Item name updated and shop updated.')
    
