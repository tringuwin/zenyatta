
import constants

async def get_shop_channel(message):
    guild = message.guild
    channel = await guild.fetch_channel(constants.SHOP_CHANNEL_ID)
    return channel


async def get_shop_message(the_shop, channel, message_id_label):
    
    if message_id_label in the_shop:

        shop_msg = await channel.fetch_message(the_shop[message_id_label])
        return shop_msg

guide_string = '-------------------------------\n'
guide_string += '**HOW TO EARN TOKENS**\n'
guide_string += '-------------------------------\n'
guide_string += '- Prizes for participating in events\n'
guide_string += '- Gift command once every 8 hours (!gift)\n'
guide_string += '- Use Twitch "Sauce Points" (Look under the twitch chat and find custom rewards)\n'
guide_string += '- Subscribe on Twitch (🪙 200)\n'
guide_string += '- Gift a sub on Twitch (🪙 200)\n'
guide_string += '- Invite a friend to this server (🪙 30 for you and 🪙 30 for your friend) **[To claim have your friend DM me that you invited them]**\n'

async def update_shop_handler(db, message):

    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 1})

    channel = await get_shop_channel(message)
    offer_msg = await get_shop_message(the_shop, channel, 'offers_message_id')
    guide_msg = await get_shop_message(the_shop, channel, 'guide_message_id')

    offers_string = '-------------------------------\n**AVAILABLE REWARDS**\n-------------------------------\n'

    offer_num = 1
    for offer in the_shop['offers']:
        offers_string += '**'+str(offer_num)+'.** '+offer['item_name']+' : **'+str(offer['price'])+' Tokens** : In Stock: ['+str(offer['in_stock'])+']\n'
        offers_string += '*To buy, use the command* **!buy '+str(offer_num)+'**\n'
        offers_string += '----------\n'
        offer_num += 1

    await offer_msg.edit(content=offers_string)
    await guide_msg.edit(content=guide_string)

    # offer_msg = await channel.send(offers_string)
    # guide_msg = await channel.send(guide_string)

    # shop.update_one({"shop_id": 1}, {"$set": {"offers_message_id": offer_msg.id}})
    # shop.update_one({"shop_id": 1}, {"$set": {"guide_message_id": guide_msg.id}})
        