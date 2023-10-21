import random

hero_list = ['Ana', 'Ashe']

async def which_hero_handler(message):

    random_hero = random.choice(hero_list)
    await message.reply(random_hero)