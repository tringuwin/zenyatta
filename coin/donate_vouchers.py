

from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from safe_send import safe_send
from user.user import get_user_vouchers, user_exists


async def donate_vouchers(db, message, context):

    message_mentions = message.mentions

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return

    if len(message_mentions) != 1:
        await safe_send(message.channel, "Please mention exactly one user to donate vouchers to.")
        return
    
    donate_discord_user = message_mentions[0]
    donate_user = user_exists(db, donate_discord_user.id)
    if not donate_user:
        await safe_send(message.channel, 'That user is not registered yet.')
        return
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    num_vouchers_to_donate = params[2]
    if not can_be_int(num_vouchers_to_donate):
        await safe_send(message.channel, f'"{num_vouchers_to_donate}" is not a valid number of vouchers to donate.')
        return
    
    num_vouchers_to_donate = int(num_vouchers_to_donate)
    if num_vouchers_to_donate <= 0:
        await safe_send(message.channel, 'You can only donate a positive number of vouchers.')
        return
    
    user_vouchers = get_user_vouchers(user)
    if user_vouchers < num_vouchers_to_donate:
        await safe_send(message.channel, f'You only have {user_vouchers} vouchers to donate.')
        return
    
    donate_user_vouchers = get_user_vouchers(donate_user)

    users = db['users']
    users.update_one({'discord_id': message.author.id}, {'$set': {'vouchers': user_vouchers - num_vouchers_to_donate}})
    users.update_one({'discord_id': donate_user['discord_id']}, {'$set': {'vouchers': donate_user_vouchers + num_vouchers_to_donate}})

    await safe_send(message.channel, 'Voucher donation successful!')

