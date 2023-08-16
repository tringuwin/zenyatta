
async def update_shop_handler(db, message):

    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 1})

    for offer in the_shop['offers']:
        await message.channel.send(offer['item_name'])
        