
import constants
from shop import update_shop

async def update_shop_handler(db, message):

    await update_shop(db, message)

    await message.channel.send('Shop updated')
        