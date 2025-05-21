

from common_messages import not_registered_response
from user.user import get_user_money, user_exists


async def money(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(user)
        return
    
    user_money_raw = get_user_money(user)
    rounded_money = round(user_money_raw, 2)

    await message.reply('Your current balance is: $'+str(rounded_money))

    