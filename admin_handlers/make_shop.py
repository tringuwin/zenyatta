

from safe_send import safe_send


async def make_shop_handler(db, message):
    
    shop = db['shop']
    new_shop = {
        'shop_id': 2,
        'offers': [],
        'offers_message_id': 1187063565039976589
    }
    shop.insert_one(new_shop)

    await safe_send(message.channel, 'Shop has been created.')