
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from rewards import change_tokens
from user import get_user_tokens, user_exists


async def donate_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    num_tokens_to_give = params[2]
    if not can_be_int(num_tokens_to_give):
        await message.channel.send('Please enter a number for how many tokens to donate.')
        return
    
    int_tokens = int(num_tokens_to_give)
    if int_tokens <= 0:
        await message.channel.send("What? Umm, no you can't do that.")

    user_tokens = get_user_tokens(user)
    if user_tokens < int_tokens:
        await message.channel.send('You do not have enough tokens for this donation.')
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
    
    await change_tokens(db, user, -1*int_tokens)
    await change_tokens(db, donate_to_user, int_tokens)
    await message.channel.send('Donation successful!')
