
import constants
from safe_send import safe_send
from shop import update_shop

async def update_shop_handler(db, message):

    await update_shop(db, message)

    await safe_send(message.channel, 'Shop updated')
