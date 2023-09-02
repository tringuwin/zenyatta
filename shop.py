import constants


async def get_shop_channel(message):
    guild = message.guild
    channel = await guild.fetch_channel(constants.SHOP_CHANNEL_ID)
    return channel

async def get_redemptions_channel(message):
    guild = message.guild
    channel = await guild.fetch_channel(constants.OFFER_REDEMPTIONS_CHANNEL_ID)
    return channel

async def get_shop_message(the_shop, channel, message_id_label):
    
    if message_id_label in the_shop:

        shop_msg = await channel.fetch_message(1141808871652987064)
        return shop_msg

guide_string = '\n-------------------------------\n'
guide_string += '**HOW TO EARN TOKENS**\n'
guide_string += '-------------------------------\n\n'
guide_string += '- Prizes for participating in events\n'
guide_string += '- Gift command once every 8 hours (!gift)\n'
guide_string += '- Use Twitch "Sauce Points" (Look under the twitch chat and find custom rewards)\n'
guide_string += '- Subscribe on Twitch (🪙 300)\n'
guide_string += '- Gift a sub on Twitch (🪙 300)\n'
guide_string += '- Invite a friend to this server (🪙 100 for you and 🪙 100 for your friend) **[DM SpicyRagu to claim when your friend joins]**\n'

async def update_shop(db, message):
    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 1})

    channel = await get_shop_channel(message)
    offer_msg = await get_shop_message(the_shop, channel, 'offers_message_id')

    offers_string = '-------------------------------\n**AVAILABLE REWARDS**\n-------------------------------\n'

    offer_num = 1
    for offer in the_shop['offers']:

        in_stock = offer['in_stock']
        if in_stock > 0:

            offers_string += '\n**'+str(offer_num)+'.** '+offer['item_name']+' : **'+str(offer['price'])+' Tokens** : ['+str(offer['in_stock'])+'] in stock\n'
            offers_string += '*To buy, use the command* **!buy '+str(offer_num)+'**\n'

        else:

            offers_string += '\n**'+str(offer_num)+'.** ~~'+offer['item_name']+' : '+str(offer['price'])+' Tokens~~ : OUT OF STOCK\n'

        offer_num += 1

    await offer_msg.edit(content=offers_string+guide_string)