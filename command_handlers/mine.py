
from common_messages import not_registered_response
from rewards import change_tokens
from user import get_user_tokens, user_exists
import random


results = {
    'Copper': 3,
    'Silver': 5,
    'Gold':25,
    'Sapphire': 30,
    'Ruby': 60,
    'Emerald': 100,
    'Diamond': 200,
    'Sauce Stone': 2000
}

async def mine_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    tokens = get_user_tokens(user)
    if tokens < 20:
        await message.channel.send('Mining costs 20 tokens. Please try again once you have 20 tokens.')
        return
    
    change_in_tokens = -20

    random_result = random.randint(1, 1000)
    result = None
    if random_result <= 400:
        result = 'Copper'
    elif random_result <= 700:
        result = 'Silver'
    elif random_result <= 830:
        result = 'Gold'
    elif random_result <= 910:
        result = 'Sapphire'
    elif random_result <= 950:
        result = 'Ruby'
    elif random_result <= 985:
        result = 'Emerald'
    elif random_result <= 999:
        result = 'Diamond'
    elif random_result == 1000:
        result = 'Sauce Stone'

    payout = results[result]
    net_change = change_in_tokens + payout

    await change_tokens(db, user, net_change)

    final_string = message.author.mention+' You paid 20 Tokens to go mining...\n'
    final_string += 'You found **'+result+"**! You sold it for **"+str(payout)+' Tokens**'

    await message.channel.send(final_string)



