
from common_messages import invalid_number_of_params, not_registered_response
from helpers import can_be_int, valid_number_of_params
from user import get_user_tokens, user_exists
import random

valid_bets = ['red', 'black', 'green']

wheel = ['red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'red', 'black', 'red', 'black',
         'green']

color_to_emoji = {
    'black': '⬛',
    'red': '🟥',
    'green': '🟩'
}

def get_roulette_details():
    
    random_start_index = random.randint(0, 36)

    spin_array = []
    for i in range (0, 9):
        spin_array.append(wheel[random_start_index])
        random_start_index += 1
        if random_start_index >= len(wheel):
            random_start_index = 0

    spin_result = spin_array[4]

    return {'array': spin_array, 'result': spin_result}


def roulette_spin_to_emojis(spin_array):

    final_string = '⬜⬜⬜⬜⬇️⬜⬜⬜⬜\n'

    for color in spin_array:
        final_string += color_to_emoji[color]

    final_string += '\n⬜⬜⬜⬜⬆️⬜⬜⬜⬜'

    return final_string

async def wager_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 3)
    if valid_params:

        user = user_exists(db, message.author.id)
        if not user:
            await not_registered_response(message)
            return

        wager = params[1]
        if not can_be_int(wager):
            await message.channel.send('Please enter a numerical value for your wager')
            return
        wager = int(wager)

        if wager > 100 or wager < 1:
            await message.channel.send('Wager must be between 1 and 100 tokens')
            return
        
        user_tokens = get_user_tokens(user)
        if user_tokens < wager:
            await message.channel.send('You do not have enough tokens for this wager')

        # CHECK VALID BET

        # TAKE TOKENS
        roulette_details = get_roulette_details()
        print(roulette_details['array'])
        print(roulette_details['result'])
        
        spin_response = roulette_spin_to_emojis(roulette_details['array'])
        await message.channel.send(spin_response)
    else:
        await invalid_number_of_params(message)