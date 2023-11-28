
from common_messages import invalid_number_of_params, not_registered_response
import constants
from helpers import valid_number_of_params
from user import get_league_team, user_exists

async def rival_of_handler(db, message):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    raw_team = params[1]
    found_team = None
    for team in constants.TEAM_LIST:
        if team.lower() == raw_team.lower():
            found_team = team
            break

    if not found_team:
        await message.channel.send('There is no team named '+str(raw_team))
        return
    
    league_team = get_league_team(user)
    if (league_team != 'None') and (league_team == found_team):
        await message.channel.send('You are a member of the team '+league_team+' so it cannot be your rival!')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"rival_of": found_team}})

    await message.channel.send("Success! You're now a rival of "+found_team)