
import copy
from helpers import get_constant_value
import uuid

SEASON_5_PICK_ARRAY = {
    'round1': ['None', 'None', 'None', 'None'],
    'round2': ['None', 'None', 'None', 'None'],
    'round3': ['None', 'None'],
    'round4': ['None'],
    'loserScore': -1,
}

SEASON_TO_PICK_ARRAY = {
    5: SEASON_5_PICK_ARRAY
}



def make_or_fetch_user_picks(picks_db, league_season, user, can_edit_picks):

    picks_obj = picks_db.find_one({'season': league_season, 'user_id': user.id})
    if not picks_obj:

        if not can_edit_picks:
            return None

        blank_picks = copy.deepcopy(SEASON_TO_PICK_ARRAY[league_season])

        picks_obj = {
            'user_id': user.id,
            'season': league_season,
            'picks': blank_picks,
            'token': str(uuid.uuid4()),
            'complete': False,
            'score': 0
        }

        picks_db.insert_one(picks_obj)
    
    return picks_obj


async def picks_handler(db, message):

    picks_active = get_constant_value(db, 'picks_active')
    if not picks_active:
        await message.channel.send('There are no pick contests available right now. Check back soon!')
        return
    
    can_edit_picks = get_constant_value(db, 'can_edit_picks')

    league_season = get_constant_value(db, 'league_season')
    picks_db = db['picks']

    user_picks = make_or_fetch_user_picks(picks_db, league_season, message.author, can_edit_picks)
    if not user_picks:
        await message.channel.send('Picks cannot be edited right now. Make sure to enter the next challenge.')
        return

    picks_message = "Use this link to edit your picks. Don't share this link with anyone, or they'll be able to edit your picks!\n\nhttps://spicyragu.netlify.app/sol/picks/"+user_picks['token']

    try:
        await message.author.send(picks_message)
        await message.channel.send('I DMed you a secure link to edit your picks!')
    except:
        await message.channel.send("I tried to send you a link to edit your picks, but it didn't work. Maybe check your privacy settings.")
