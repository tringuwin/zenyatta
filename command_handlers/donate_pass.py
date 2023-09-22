
from datetime import datetime, timezone
import math
from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_params_ignore_whitespace
from rewards import change_passes
from user import get_user_passes, user_exists
import constants


async def donate_pass_handler(db, message):

    valid_params, params = valid_params_ignore_whitespace(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return

    user_passes = get_user_passes(user)
    if user_passes < 1:
        await message.channel.send('You do not have enough passes for this donation.')
        return
    
    account_age = datetime.now(timezone.utc) - message.author.created_at
    account_days = account_age.days
    if account_days < 30:
        account_days = int(math.floor(account_days))
        await message.channel.send('Your Discord account is **'+str(account_days)+' days** old. To prevent alt account spam, only accounts 30 days or older can use the donate command.')
        return

    mentions = message.mentions
    if len(mentions) != 1:
        await message.channel.send('Please mention 1 player to donate to.')
        return
    
    mentioned_user = mentions[0]
    donate_to_user = user_exists(db, mentioned_user.id)
    if not donate_to_user:
        await message.channel.send('That user is not registered yet.')
        return
    
    if donate_to_user == user:
        await message.channel.send("You can't donate to yourself...")
        return
    
    if donate_to_user['discord_id'] == constants.SPICY_RAGU_ID:
        await message.channel.send("Thank you! But Spicy doesn't need passes since he owns the server!")
        return
    
    await change_passes(db, user, -1)
    await change_passes(db, donate_to_user, 1)
    await message.channel.send('Donation successful!')