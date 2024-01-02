
from league import validate_admin


async def toggle_apps_handler(db, message):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return

    apps = db['applications']
    apps_obj = apps.find_one({'teams_id': 1})
    apps_teams = apps_obj['teams']

    current_value = True

    for team in apps_teams:
        if team['team'] == team_name:

            if team['appsLink'] == 'None':
                await message.channel.send(message.author.mention+" You need to set the Google Form link for your team's applications before using this command. (Use **!setappslink LinkHere**)")
                return

            team['appsOpen'] = not team['appsOpen']
            current_value = team['appsOpen']
            break

    apps.update_one({"teams_id": 1}, {"$set": {"teams": apps_teams}})
    if current_value:
        await message.channel.send('Applications for '+team_name+' are now **ON**')
    else:
        await message.channel.send('Applications for '+team_name+' are now **OFF**')