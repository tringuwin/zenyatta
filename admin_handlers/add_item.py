

from helpers import make_string_from_word_list
from shop import update_shop


async def add_item_handler(db, message):
    
    word_list = message.content.split(' ')
    price = int(word_list[1])
    in_stock = int(word_list[2])
    auto = int(word_list[3])

    item_name = make_string_from_word_list(word_list, 4)

    if auto == 1:
        auto = True
    else:
        auto = False


    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 2})

    new_offer = {
        'item_name': item_name,
        'price': price,
        'in_stock': in_stock,
        'auto': auto
    }

    the_shop['offers'].append(new_offer)
    shop.update_one({"shop_id":2}, {"$set": {"offers": the_shop['offers']}})

    await update_shop(db, message)

    await message.channel.send('Item added and shop updated.')