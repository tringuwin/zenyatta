
from common_messages import invalid_number_of_params, not_registered_response
from teams import get_team_by_name, make_team
from user import user_exists


async def make_team_handler(db, message): 

    word_list = message.content.split(' ')
    if len(word_list) > 2:

        user = user_exists(db, message.author.id)
        if user:
             
            team_size = int(word_list[1])
            team_name = ''

            team_name_section_index = 2
            while team_name_section_index < len(word_list):
                team_name += word_list[team_name_section_index]
                team_name_section_index += 1
                if team_name_section_index != len(word_list):
                    team_name += ' '

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
        
            
        

    
    
    