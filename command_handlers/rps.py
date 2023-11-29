

from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from rewards import change_tokens
from user import get_user_tokens, user_exists

import random

VALID_RPS = ['Rock', 'Paper', 'Scissors']

RPS_TO_EMOJI = {

    'Rock': '🪨',
    'Paper': '📄',
    'Scissors': '✂️'

}

async def rps_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    bet = params[1]
    if not can_be_int(bet):
        await message.channel.send(bet+' is not a number')
        return
    
    bet = int(bet)
    if bet > 1000 or bet < 10:
        await message.channel.send('Your bet must be a number between 10 and 1000.')
        return
    
    user_tokens = get_user_tokens(user)
    if user_tokens < bet:
        await message.channel.send('You do not have enough tokens for this bet.')
        return
    
    icon = params[2]
    is_valid = False
    normalized = None
    for valid_icon in VALID_RPS:
        if valid_icon.lower() == icon.lower():
            normalized = valid_icon
            is_valid = True
            break

    if not is_valid:
        await message.channel.send(icon+' is not valid. You must say rock, paper, or scissors.')
        return
    
    zen_choice = random.choice(VALID_RPS)

    final_string = message.author.mention+'\n'
    final_string += 'You chose '+RPS_TO_EMOJI[normalized]+' **'+normalized+'**\n'
    final_string += 'And I choose...\n'
    final_string += RPS_TO_EMOJI[zen_choice]+' **'+zen_choice+'!**\n'
    final_string += '-------------\n'

    is_tie = False
    zen_won = True

    if zen_choice == normalized:
        is_tie = True
    else:
        if normalized == 'Rock' and zen_choice == 'Scissors':
            zen_won = False
        elif normalized == 'Paper' and zen_choice == 'Rock':
            zen_won = False
        elif normalized == 'Scissors' and zen_choice == 'Paper':
            zen_won = False

    if is_tie:
        final_string += "It's a **Tie**! You get your bet back."
    elif zen_won:
        final_string += 'You lose. You lost '+str(bet)+' tokens.'
        await change_tokens(db, user, -1*bet)
    else:
        payout_raw = float(bet) * 0.9
        payout_int = int(payout_raw)
        final_string += 'You win! You won **'+str(payout_int)+' Tokens!**'
        await change_tokens(db, user, payout_int)

    await message.channel.send(final_string)


    

    
