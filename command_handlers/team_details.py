
from common_messages import invalid_number_of_params
from teams import get_team_by_name, make_team_name_from_word_list
from user import user_exists

def make_details_from_team(db, team):
    
    team_owner = user_exists(db, team['creator_id'])

    team_string = '**Team Owner:** '+team_owner['battle_tag']+'\n'
    team_string += '**Team Size:** '+str(team['team_size'])+'\n'

    return team_string

async def team_details_hanlder(db, message):
    
    word_list = message.content.split(' ')
    if len(word_list) > 1:

        team_name = make_team_name_from_word_list(word_list, 1)
        existing_team = await get_team_by_name(db, team_name)
        if existing_team:
            team_details = make_details_from_team(db, existing_team)
            await message.channel.send(team_details)
        else:
            await message.channel.send('There is no team with the name "'+team_name+'"')

    else:
        await invalid_number_of_params(message)