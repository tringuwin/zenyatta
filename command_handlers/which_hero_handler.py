import random
import constants


ALL_HEROES = ['Mauga', 'Ana', 'Ashe', 'Baptiste', 'Bastion', 'Brigitte', 'Cassidy', 'D.va', 'Doomfist', 'Echo', 'Genji', 
              'Hanzo', 'Illari', 'Junker Queen', 'Junkrat', 'Kiriko', 'Lifeweaver', 'Lucio', 'Mei', 'Mercy', 'Moira', 
              'Orisa', 'Pharah', 'Ramattra', 'Reaper', 'Reinhardt', 'Roadhog', 'Sigma', 'Sojourn', 'Soldier: 76', 
              'Sombra', 'Symmetra', 'Torbjorn', 'Tracer', 'Widowmaker', 'Winston', 'Wrecking Ball', 'Zarya', 'Zenyatta']

async def which_hero_handler(message):

    await message.reply(random.choice(ALL_HEROES))