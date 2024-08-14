
import constants
from discord_actions import get_guild
from helpers import get_constant_value, set_constant_value


async def end_vote_handler(db, message, client):

    current_vote = get_constant_value(db, 'sub_vote')

    if not current_vote['active']:
        await message.channel.send('There is no current vote.')
        return
    
    winning_option = None
    winning_votes = None
    tie = False

    for option in current_vote['options']:

        if (not winning_option) or (option['votes'] > winning_votes):
            winning_option = option['name']
            winning_votes = option['votes']
            tie = False

        elif option['votes'] == winning_votes:
            tie = True

    current_vote['active'] = False
    set_constant_value(db, 'sub_vote', current_vote)

    guild = await get_guild(client)
    vote_channel = guild.get_channel(constants.SUB_VOTE_CHANNEL)

    if tie:
        await vote_channel.send('The vote is a tie! Spicy will be the tie breaker.')
    else:
        await vote_channel.send('The vote is over! The winning option is **'+winning_option+'** !!!')

    await message.channel.send('Vote ended')

        