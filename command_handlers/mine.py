
from common_messages import not_registered_response
from discord_actions import get_guild
from rewards import change_pickaxes, change_tokens
from user import get_user_gems, get_user_pickaxes, get_user_tokens, user_exists
import random
import constants


results = {
    'Copper': 3,
    'Silver': 5,
    'Gold': 25,
    'Sapphire': 30,
    'Ruby': 60,
    'Emerald': 100,
    'Diamond': 200,
    'Sauce Stone': 2000
}

flair = {
    'Copper': '🟤',
    'Silver': '⚪️',
    'Gold': '🟡',
    'Sapphire': '🔵',
    'Ruby': '🔴',
    'Emerald': '🟢',
    'Diamond': '💎',
    'Sauce Stone': '🍅'
}


async def mine_handler(db, message, client):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    valid_mine = False
    mine_was_pickaxe = False

    user_pickaxes = get_user_pickaxes(user)

    change_in_tokens = -20

    if user_pickaxes > 0:
        valid_mine = True
        mine_was_pickaxe = True
        change_in_tokens = 0
        await change_pickaxes(db, user, -1)

    tokens = get_user_tokens(user)
    if (not valid_mine) and tokens < 20:
        await message.channel.send('Mining costs 20 tokens or a Pickaxe. Please try again once you have 20 tokens or a Pickaxe.')
        return

    random_result = random.randint(1, 1000)
    result = None
    is_gem = False
    gem_color = None
    if random_result <= 500:
        result = 'Copper'
    elif random_result <= 769:
        result = 'Silver'
    elif random_result <= 859:
        result = 'Gold'
    elif random_result <= 894:
        result = 'Sapphire'
    elif random_result <= 919:
        result = 'Ruby'
    elif random_result <= 939:
        result = 'Emerald'
    elif random_result <= 949:
        result = 'Diamond'
    elif random_result <= 999:
        result = 'Gem'
        is_gem = True
        gem_color = random.choice(constants.GEM_COLORS)
    elif random_result == 1000:
        result = 'Sauce Stone'


    if is_gem:
        payout = 0
        my_gem_id = constants.COLOR_TO_EMOJI_ID[gem_color]
        guild = await get_guild(client)
        gem_emoji = guild.get_emoji(my_gem_id)
        my_flair = str(gem_emoji)
        user_gems = get_user_gems(user)
        user_gems[gem_color] += 1
        users = db['users']
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}})
    else:
        payout = results[result]
        my_flair = flair[result]


    net_change = change_in_tokens + payout
    await change_tokens(db, user, net_change, 'mineshaft')

    final_string = ''
    if mine_was_pickaxe:
        final_string += message.author.mention+' You used a Pickaxe Item ⛏️ to go mining...\n'
    else:
        final_string += message.author.mention+' You paid 20 Tokens to go mining...\n'

    if is_gem:
        final_string += 'You found '+str(my_flair)+' **'+result+"** "+str(my_flair)+" !"
    else:
        final_string += 'You found '+str(my_flair)+' **'+result+"** "+str(my_flair)+" ! You sold it for **"+str(payout)+' Tokens**'

    await message.channel.send(final_string)



