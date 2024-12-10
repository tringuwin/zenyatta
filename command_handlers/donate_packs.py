
import constants
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_params_ignore_whitespace
from rewards import change_packs
from user import get_user_packs, user_exists


async def donate_packs(db, message):

    valid_params, params = valid_params_ignore_whitespace(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    num_packs_to_give = params[2]
    if not can_be_int(num_packs_to_give):
        await message.channel.send('Please enter a number for how many packs to donate. Has to be a whole number.')
        return
    
    int_packs = int(num_packs_to_give)
    if int_packs <= 0:
        await message.channel.send("What? Umm, no you can't do that.")
        return

    user_packs = get_user_packs(user)
    if user_packs < int_packs:
        await message.channel.send('You do not have enough packs for this donation.')
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
    
    if donate_to_user['discord_id'] == constants.ZEN_ID:
        await message.channel.send("Thank you! But I don't need any packs!")
        return
    
    await change_packs(db, user, -1*int_packs)
    await change_packs(db, donate_to_user, int_packs)
    await message.channel.send('Donation successful!')