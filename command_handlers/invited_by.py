
from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from rewards import change_tokens
from safe_send import safe_send
from user.user import get_invited_valid, user_exists
import constants

invited_by_blacklist = [
    0,
    # 513207840878624776, #kaz
    # 607788667833942035 #lucioisblack
]

async def invited_by_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    valid_params, params = valid_number_of_params(message, 2)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    invited_valid = get_invited_valid(user)
    if not invited_valid:
        await safe_send(message.channel, 'You are not allowed to use this command. (Either you have already used it, or you joined before this command existed)')
        return
    
    mentions = message.mentions
    if len(mentions) != 1:
        await safe_send(message.channel, 'Please mention the user that invited you.')
        return
    
    inviter = mentions[0]
    inviter_user = user_exists(db, inviter.id)
    if not inviter_user:
        await safe_send(message.channel, 'This user is not registered yet. You cannot use this command until they register.')
        return
    
    if inviter_user['discord_id'] == user['discord_id']:
        await safe_send(message.channel, "You can't invite yourself...")
        return
    
    if inviter_user['discord_id'] == constants.SPICY_RAGU_ID:
        await safe_send(message.channel, 'Sorry, SpicyRagu does not count as a valid inviter!')
        return
    
    on_black_list = False
    for black in invited_by_blacklist:
        if black == inviter_user['discord_id']:
            on_black_list = True
            break

    if on_black_list:
        await safe_send(message.channel, 'That user is not allowed to recieve token bonuses for inviting due to abusing this command.')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"invited_valid": False}})
    await change_tokens(db, user, 100, 'invited-by')
    await change_tokens(db, inviter_user, 100, 'invited-by')

    await safe_send(message.channel, 'Success! You and your inviter both got 100 bonus tokens! 🪙')
