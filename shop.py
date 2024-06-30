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

        shop_msg = await channel.fetch_message(1187064592342462525)
        return shop_msg

guide_string = '\n**HOW TO EARN TOKENS**\n'
guide_string += '- Prizes for participating in events\n'
guide_string += '- Gift command once every 8 hours (!gift)\n'
guide_string += '- Use Twitch "Sauce Points" (Look under the twitch chat and find custom rewards)\n'
guide_string += '- Invite a friend to the server. (🪙 100 Tokens for you AND 🪙 100 for your friend) Have the person you invited say **!invitedby @You**\n'
guide_string += '- Use this link to purchase any "Rogue Energy" products. (Link also provides 20% discount) Every 5 cents you spend using this link, gives you 1 Token. (Also gives Card Packs! DM SpicyRagu your order number to claim) https://rogueenergy.com/discount/Spicy?ref=dmxeauce'  

async def update_shop(db, message):
    shop = db['shop']
    the_shop = shop.find_one({'shop_id': 2})

    channel = await get_shop_channel(message)
    offer_msg = await get_shop_message(the_shop, channel, 'offers_message_id')

    offers_string = '***The Token Shop can only be used by Twitch Subscribers. The Token Shop is Re-Stocked at around noon EST each Friday.*** (To Access, subscribe here: https://www.twitch.tv/spicyraguow )\n'
    offers_string += '*Prices for these items change on a weekly basis. If an item fully sells out, the price is raised 100 tokens, otherwise, the price is lowered 100 tokens.*\n\n'
    offers_string += '-------------------------------\n**AVAILABLE REWARDS**\n-------------------------------\n'

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