
from datetime import datetime, timezone
from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from rewards import change_passes
from user import get_user_passes, user_exists


async def donate_pass_handler(db, message):

    valid_params, params = valid_number_of_params(message, 2)
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
    if account_days < 60:
        await message.channel.send('Your discord account was created less than 60 days ago. To prevent alt account spam, only accounts 60 days or older can use the donate command.')
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
    
    await change_passes(db, user, -1)
    await change_passes(db, donate_to_user, 1)
    await message.channel.send('Donation successful!')