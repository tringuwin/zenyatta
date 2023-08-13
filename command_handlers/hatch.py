
from common_messages import not_registered_response
from rewards import change_eggs
from user import user_exists
import discord
import random


def get_creature_id():
    id = random.randint(1, 2)
    return id

def get_creature_image(creature_id):
    pass

async def hatch_handler(db, message):

    user = user_exists(db, message.author.id)
    if user:

        if 'eggs' in user and user['eggs'] > 0:
            await change_eggs(db, user, -1)
            creature_id = get_creature_id()
            creature_file = discord.File('spicemon/S'+str(creature_id)+'.png', filename='spicemon.png')
            creature_embed = discord.Embed(title='You hacthed creature '+str(creature_id))
            creature_embed.set_image(url='attachment://spicemon.png')
            await message.channel.send(file=creature_file, embed=creature_embed)
        else:
            await message.channel.send('You do not have any eggs right now.')

    else:
        await not_registered_response(message)