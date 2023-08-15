
from common_messages import invalid_number_of_params, not_registered_response
from teams import get_team_by_name, make_team, make_team_name_from_word_list
from user import user_exists
import constants

def can_be_int(var):
    try:
        int(var)
        return True
    except ValueError:
        return False

async def make_team_handler(db, message): 

    word_list = message.content.split(' ')
    if len(word_list) > 2:

        user = user_exists(db, message.author.id)
        if user:

            if len(user['teams']) >= constants.MAX_PLAYER_TEAMS:
                await message.channel.send('You are already on '+str(constants.MAX_PLAYER_TEAMS)+' which is the max allowed.')
                return

            if not can_be_int(word_list[1]):
                await message.channel.send('Please include the number of players in the team in the command.')
                return

            team_size = int(word_list[1])
            if team_size > 5 or team_size < 2:
                await message.channel.send('Invalid team size. Teams must have between 2-5 players.')
                return

            team_name = make_team_name_from_word_list(word_list, 2)
            if len(team_name) > 30:
                await message.channel.send('Team name must be 30 characters or less.')
            else:

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
        
            
        

    
    
    