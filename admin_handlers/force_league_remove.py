

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params
from safe_send import safe_send


async def force_league_remove_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name = params[1]
    user_id = int(params[2])

    league_teams = db['leagueteams']
    team_object = league_teams.find_one({'team_name': team_name})
    
    final_members = []
    for member in team_object['members']:
        if member['discord_id'] != user_id:
            final_members.append(member)

    league_teams = db['leagueteams']
    league_teams.update_one({'team_name': team_name}, {"$set": {"members": final_members}})

    users = db['users']
    users.update_one({"discord_id": user_id}, {"$set": {"league_team": 'None'}})

    team_object['members'] = final_members

    await safe_send(message.channel, "User was kicked from the league team.")