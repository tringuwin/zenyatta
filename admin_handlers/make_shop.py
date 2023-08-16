

async def make_shop_handler(db, message):
    
    shop = db['shop']
    new_shop = {
        'shop_id': 1,
        'offers': []
    }
    shop.insert_one(new_shop)

    await message.channel.send('Shop has been created.')