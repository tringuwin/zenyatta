import random
import constants
from safe_send import safe_reply

async def which_team_handler(message):

    random_team = random.choice(constants.TEAM_LIST)
    await safe_reply(message, random_team)