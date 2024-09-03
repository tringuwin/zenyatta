

from command_handlers.league.update_team import update_team
from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params
from league import validate_admin


async def league_order_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    valid_admin, team, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return

    first_spot = params[1]
    if not can_be_int(first_spot):
        await message.channel.send(first_spot+' is not a number')
        return
    first_spot = int(first_spot)
    
    second_spot = params[2]
    if not can_be_int(second_spot):
        await message.channel.send(second_spot+' is not a number')
        return
    second_spot = int(second_spot)
    
    team_members = team['members']
    team_length = len(team_members)
    
    if first_spot > team_length:
        await message.channel.send(str(first_spot)+' is too high. There is only '+str(team_length)+' players on your team.')
        return
    
    if second_spot > team_length:
        await message.channel.send(str(second_spot)+' is too high. There is only '+str(team_length)+' players on your team.')
        return
    
    if first_spot < 1:
        await message.channel.send(str(first_spot)+' is invalid. It must be a positive number.')
        return
    
    if second_spot < 1:
        await message.channel.send(str(second_spot)+' is invalid. It must be a positive number.')
        return
    
    first_spot -= 1
    second_spot -= 1

    hold_first = team_members[first_spot]
    team_members[first_spot] = team_members[second_spot]
    team_members[second_spot] = hold_first

    teams_db = db['leagueteams']
    teams_db.update_one({"team_name": team_name}, {"$set": {"members": team_members}})

    await message.channel.send('Please wait... This may take a while...')
    
    await update_team(db, team_name, client)

    await message.channel.send(team_name+' was updated.')