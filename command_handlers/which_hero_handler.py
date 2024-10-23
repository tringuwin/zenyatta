import random
import constants


ALL_HEROES = ['Ana', 'Ashe', 'Baptiste', 'Bastion', 'Brigitte', 'Cassidy', 'D.va', 'Doomfist', 'Echo', 'Genji', 
              'Hanzo', 'Illari', 'Junker Queen', 'Junkrat', 'Juno', 'Kiriko', 'Lifeweaver', 'Lucio', 'Mauga', 'Mei', 'Mercy', 'Moira', 
              'Orisa', 'Pharah', 'Ramattra', 'Reaper', 'Reinhardt', 'Roadhog', 'Sigma', 'Sojourn', 'Soldier: 76', 
              'Sombra', 'Symmetra', 'Torbjorn', 'Tracer', 'Venture', 'Widowmaker', 'Winston', 'Wrecking Ball', 'Zarya', 'Zenyatta']

async def which_hero_handler(message):

    await message.reply(random.choice(ALL_HEROES))