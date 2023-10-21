import random

hero_list = ['Ana', 'Ashe', 'Baptiste', 'Bastion', 'Brigitte', 'Cassidy',
             'D.va', 'Doomfist', 'Echo', 'Gneji', 'Hanzo', 'Illari',
             'Junker Queen', 'Junkrat', 'Kiriko', 'Lifeweaver', 'Lucio', 'Mei',
             'Mercy', 'Moira', 'Orisa', 'Pharah', 'Ramattra', 'Reaper',
             'Reinhardt', 'Roadhog', 'Sigma', 'Sojourn', 'Soldier: 76', 'Sombra',
             'Symmetra', 'Torbjorn', 'Tracer', 'Widowmaker', 'Winston', 'Wrecking Ball',
             'Zarya', 'Zenyatta']

async def which_hero_handler(message):

    random_hero = random.choice(hero_list)
    await message.reply(random_hero)