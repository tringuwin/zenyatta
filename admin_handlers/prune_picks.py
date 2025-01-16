

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


def pick_is_done(picks):

    for i in range(1, 5):
        picks_round = picks['round'+str(i)]
        for pick in picks_round:
            if pick == 'None':
                return False
    
    if picks['loserScore'] == -1:
        return False

    return True



async def prune_picks(db, message):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    season = int(params[1])

    picks_db = db['picks']

    all_picks_in_season = picks_db.find({'season': season})

    pick_ids_to_delete = []
    for pick in all_picks_in_season:
        if not pick_is_done(pick['picks']):
            pick_ids_to_delete.append(pick['token'])

    print(pick_ids_to_delete)