

from helpers import get_constant_value


SEASON_5_PICK_ARRAY = {
    'round1': ['None', 'None', 'None', 'None'],
    'round2': ['None', 'None', 'None', 'None'],
    'round3': ['None', 'None'],
    'round4': ['None'],
    'leftScore': -1,
    'rightScore': -1
}




async def picks_handler(db, message):

    picks_active = get_constant_value(db, 'picks_active')
    if not picks_active:
        await message.channel.send('There are no pick contests available right now. Check back soon!')
        return