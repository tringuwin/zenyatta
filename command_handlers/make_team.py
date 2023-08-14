
from common_messages import invalid_number_of_params, not_registered_response
from helpers import valid_number_of_params
from teams import get_team_by_name, make_team
from user import user_exists


async def make_team_handler(db, message): 

    valid_params, params = valid_number_of_params(message, 3)
    if valid_params:
        
        user = user_exists(db, message.author.id)
        if user:
            
            team_size = int(params[1])
            team_name = params[2]
            
            existing_team = await get_team_by_name(db, team_name)
            if existing_team:
                await message.channel.send('A team with this name already exists. Try another name!')
            else:
                await make_team(db, user, team_size, team_name)
                await message.channel.send('Success! Your new team has been created.')

        else:
            await not_registered_response(message)
    else:
        await invalid_number_of_params(message)
    
    