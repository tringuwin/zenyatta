import random

hero_list = []

async def which_hero_handler(message):

    random_hero = random.choice(hero_list)
    await message.reply(random_hero)