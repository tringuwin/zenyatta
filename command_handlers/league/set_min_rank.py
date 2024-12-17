
from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from league import validate_admin


VALID_RANKS = [
    'bronze',
    'silver',
    'gold',
    'platinum',
    'diamond',
    'master',
    'grandmaster',
    'champ'
]

async def set_min_rank_handler(db, message, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    rank = params[1].lower()
    if not rank in VALID_RANKS:
        await message.channel.send('That is not a valid rank. Please enter a rank in the range bronze to champ.')
        return

    apps = db['applications']
    apps_obj = apps.find_one({'teams_id': 1})
    apps_teams = apps_obj['teams']

    found_app = False
    for team in apps_teams:
        if team['team'] == team_name:
            team['min'] = rank
            found_app = True
            break

    if not found_app:
        await message.channel.send('Was not able to set the minimum rank for this team because this team is not yet listed on the application website. If you think this is a mistake please contact the server owner.')
        return

    apps.update_one({"teams_id": 1}, {"$set": {"teams": apps_teams}})
    await message.channel.send('Application link for '+team_name+' has been updated.')