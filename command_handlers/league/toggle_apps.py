
from league import validate_admin


async def toggle_apps_handler(db, message, context):

    if context == 'MR':
        await message.channel.send('Command is not ready yet for Marvel Rivals.')
        return

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return


    team_name_lower = team_name.lower()

    league_teams = db['leagueteams']
    my_team = league_teams.find_one({'name_lower': team_name_lower})
    if not my_team:
        await message.channel.send('Was not able to set the minimum rank for this team because this team is not yet listed on the application website. If you think this is a mistake please contact the server owner.')
        return
    
    current_value = True
    if my_team['applications']['appsOpen']:
        current_value = False

    my_team['applications']['appsOpen'] = current_value
    league_teams.update_one({"name_lower": team_name_lower}, {"$set": {"applications": my_team['applications']}})

    if current_value:
        await message.channel.send('Applications for '+team_name+' are now **ON**')
    else:
        await message.channel.send('Applications for '+team_name+' are now **OFF**')