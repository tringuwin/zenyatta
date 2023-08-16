
import constants

async def get_shop_channel(message):
    guild = message.guild
    channel = await guild.fetch_channel(constants.SHOP_CHANNEL_ID)
    return channel


async def delete_shop_message_if_exists(the_shop, channel, message_id_label):
    
    if message_id_label in the_shop:

        del_msg = await channel.fetch_msg(the_shop[message_id_label])
        if del_msg:
            await del_msg.delete()

async def update_shop_handler(db, message):


    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 1})

    channel = await get_shop_channel(message)
    await delete_shop_message_if_exists(the_shop, channel, 'offers_message_id')
    await delete_shop_message_if_exists(the_shop, channel, 'guide_message_id')

    offers_string = 'this is the offers string'
    guide_string = 'this is the guide string'

    offer_msg = await channel.send(offers_string)
    guide_msg = await channel.send(guide_string)

    shop.update_one({"shop_id": 1}, {"$set": {"offers_message_id": offer_msg.id}})
    shop.update_one({"shop_id": 1}, {"$set": {"guide_message_id": guide_msg.id}})

    for offer in the_shop['offers']:
        await message.channel.send(offer['item_name'])
        