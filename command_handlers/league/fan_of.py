
from common_messages import invalid_number_of_params, not_registered_response
from context.context_helpers import get_fan_of_field_from_context, get_league_teams_collection_from_context
from helpers import valid_number_of_params
from user import user_exists

async def fan_of_handler(db, message, context):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message, context)
        return
    
    raw_team = params[1]

    league_teams = get_league_teams_collection_from_context(db, context)
    found_team = None
    found_team_object = league_teams.find_one({'name_lower': raw_team.lower()})
    if found_team_object:
        found_team = found_team_object['team_name']

    if not found_team:
        if raw_team.lower() == 'none':
            found_team = 'None'

    if not found_team:
        await message.channel.send('There is no team named '+str(raw_team))
        return
    
    users = db['users']
    fan_of_field = get_fan_of_field_from_context(context)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {fan_of_field: found_team}})

    await message.channel.send("Success! You're now a fan of "+found_team)