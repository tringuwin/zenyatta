

from common_messages import not_registered_response
from helpers import get_constant_value, set_constant_value
from safe_send import safe_send
from user.user import get_user_trophies, user_exists


async def redeem_trophies(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_trophies = get_user_trophies(user)

    if user_trophies <= 100:
        await safe_send(message.channel, f"{message.author.mention} You need at least 100 trophies to redeem for a voucher. You currently have {user_trophies} trophies.")
        return
    
    free_vouchers = get_constant_value(db, 'free_vouchers')

    if free_vouchers <= 0:
        await safe_send(message.channel, f"{message.author.mention} Sorry, there are no vouchers available for redemption at the moment. Please try again later.")
        return
    
    vouchers_to_redeem = user_trophies // 100
    vouchers_to_redeem = min(vouchers_to_redeem, free_vouchers)
    trophies_used = vouchers_to_redeem * 100

    users = db['users']
    users.update_one(
        {"discord_id": message.author.id},
        {
            "$inc": {
                "trophies": -trophies_used,
                "vouchers": vouchers_to_redeem
            }
        }
    )

    set_constant_value(db, 'free_vouchers', free_vouchers - vouchers_to_redeem)

    await safe_send(message.channel, f"{message.author.mention} Successfully redeemed {trophies_used} trophies for {vouchers_to_redeem} voucher(s). You now have {user_trophies - trophies_used} trophies and {user.get('vouchers', 0) + vouchers_to_redeem} vouchers.")