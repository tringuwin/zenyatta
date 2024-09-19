

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
from rewards import change_packs
from user import user_exists


async def gp_handler(db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    mentions = message.mentions
    if len(mentions) != 1:
        await message.channel.send('Please mention a user to give them packs.')
        return
    
    user_mentioned = mentions[0]

    num_packs = params[2]
    if not can_be_int(num_packs):
        await message.channel.send(num_packs+' is not a valid number')
        return
    num_packs = int(num_packs)

    if num_packs < 1:
        await message.channel.send('Minimum number of packs that can be given is 1')
        return
    
    user = user_exists(db, user_mentioned.id)
    if not user:
        await message.channel.send('That user is not registered, so they cannot receive packs right now.')
        return
    
    await change_packs(db, user, num_packs)
    await message.channel.send('Packs given.')
