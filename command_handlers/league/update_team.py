
from league import update_team_info


async def update_team_handler(db, message, client):

    team_name = message.content.split()[1]

    league_teams = db['leagueteams']
    team_object = league_teams.find_one({'team_name': team_name})

    if not team_object:
        await message.channel.send('Team not found')
        return
    
    await update_team_info(client, team_object, db)