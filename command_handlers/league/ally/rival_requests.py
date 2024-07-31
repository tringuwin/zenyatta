from league import validate_admin


async def rival_requests_handler(db, message):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not a team admin of a league team.')
        return

    league_teams = db['leagueteams']
    my_team = league_teams.find_one({'team_name': team_name})
    if not my_team:
        await message.channel.send('Something went very wrong.')
        return
    
    rival_reqs = my_team['rival_reqs']
    if len(rival_reqs) == 0:
        await message.channel.send('Your team does not currently have any Rival Requests from any other teams.')
        return
    
    final_string = '**RIVAL REQUESTS FOR '+team_name.upper()+'**'

    cur_index = 1
    for rival in my_team['rival_reqs']:

        final_string += '\n'+str(cur_index)+'. '+rival+' ( To accept this Rival Request, use the command **!acceptrival '+rival+'** )'

        cur_index += 1

    await message.channel.send(final_string)