
from common_messages import not_registered_response
from rewards import change_eggs
from user import user_exists
import discord
import random


gen1 = [
    [2, 3, 4, 6, 7, 9, 12, 13, 15, 17], #common
    [1, 5, 8, 10, 16], #rare
    [11, 14, 18], #mythical
    [19, 20]  #epic
]


def get_creature_id():
    id = random.randint(1, 2)
    return id

def get_creature_image(creature_id):
    pass

# 0 Common
# 1 Rare
# 2 Mythical
# 3 Epic
def get_hatch_tier():

    random_result = random.randint(1, 100)

    if random_result == 1:
        return 3
    elif random_result <= 10:
        return 2
    elif random_result <= 30:
        return 1
    else:
        return 0


def get_spicemon_from_tier(tier):

    tier_group = gen1[tier]

    random_choice = random.choice(tier_group)
    return random_choice



async def hatch_handler(db, message):

    user = user_exists(db, message.author.id)
    if user:

        if 'eggs' in user and user['eggs'] > 0:

            hatch_tier = get_hatch_tier()
            creature_id = get_spicemon_from_tier(hatch_tier)

            await change_eggs(db, user, -1)
            creature_file = discord.File('spicemon/S'+str(creature_id)+'.png', filename='spicemon.png')
            creature_embed = discord.Embed(title='You hacthed creature '+str(creature_id))
            creature_embed.set_image(url='attachment://spicemon.png')
            await message.channel.send(file=creature_file, embed=creature_embed)
        else:
            await message.channel.send('You do not have any eggs right now.')

    else:
        await not_registered_response(message)