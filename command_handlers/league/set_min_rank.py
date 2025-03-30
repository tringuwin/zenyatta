
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from league import validate_admin


VALID_RANKS_OW = [
    'bronze',
    'silver',
    'gold',
    'platinum',
    'diamond',
    'master',
    'grandmaster',
    'champ'
]

VALID_RANKS_MR = [
    'bronze',
    'silver',
    'gold',
    'platinum',
    'diamond',
    'grandmaster',
    'celestial',
    'eternity',
    'one-above-all'
]

async def set_min_rank_handler(db, message, context):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    rank = params[1].lower()

    valid_ranks = VALID_RANKS_OW if context == 'OW' else VALID_RANKS_MR

    if not rank in valid_ranks:
        await message.channel.send('That is not a valid rank. Please enter a rank in the range bronze to champ.')
        return

    team_name_lower = team_name.lower()

    league_teams = db['leagueteams']
    my_team = league_teams.find_one({'name_lower': team_name_lower})
    if not my_team:
        await message.channel.send('Was not able to set the minimum rank for this team because this team is not yet listed on the application website. If you think this is a mistake please contact the server owner.')
        return

    my_team['applications']['min'] = rank

    league_teams.update_one({"name_lower": team_name_lower}, {"$set": {"applications": my_team['applications']}})
    await message.channel.send('Application link for '+team_name+' has been updated.')