
import constants

async def get_shop_channel(message):
    guild = message.guild
    channel = await guild.fetch_channel(constants.SHOP_CHANNEL_ID)
    return channel


async def get_shop_message(the_shop, channel, message_id_label):
    
    if message_id_label in the_shop:

        shop_msg = await channel.fetch_message(the_shop[message_id_label])
        return shop_msg

async def update_shop_handler(db, message):


    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 1})

    channel = await get_shop_channel(message)
    offer_msg = await get_shop_message(the_shop, channel, 'offers_message_id')
    guide_msg = await get_shop_message(the_shop, channel, 'guide_message_id')

    offers_string = 'this is the offers string [edited 2]'
    guide_string = 'this is the guide string [EDITED 2]'

    await offer_msg.edit(content=offers_string)
    await guide_msg.edit(content=guide_string)

    # offer_msg = await channel.send(offers_string)
    # guide_msg = await channel.send(guide_string)

    # shop.update_one({"shop_id": 1}, {"$set": {"offers_message_id": offer_msg.id}})
    # shop.update_one({"shop_id": 1}, {"$set": {"guide_message_id": guide_msg.id}})

    for offer in the_shop['offers']:
        await message.channel.send(offer['item_name'])
        