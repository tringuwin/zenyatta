import random
import constants

async def which_hero_handler(message):

    random_team = random.choice(constants.TEAM_LIST)
    await message.reply('You should join the team '+random_team)