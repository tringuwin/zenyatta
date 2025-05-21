
from common_messages import invalid_number_of_params
from helpers import make_string_from_word_list
from teams import get_team_by_name
from user.user import user_exists

def make_details_from_team(db, team):
    
    team_owner = user_exists(db, team['creator_id'])

    team_string = '**'+team['team_name']+'** Details\n'
    team_string += '-----------------------------------\n'
    team_string += '**Team Owner:** '+team_owner['battle_tag']+'\n'
    team_string += '**Team Size:** '+str(team['team_size'])+'\n'
    team_string += '**Number of Players:** '+str(len(team['members']))+'/'+str(team['team_size'])+'\n'
    team_string += '-----------------------------------\n'
    team_string += 'PLAYERS\n'
    team_string += '-----------------------------------\n'

    p_index = 0
    while p_index < team['team_size']:
        player = None
        if p_index == 0:
            player = team_owner
        elif len(team['members']) > p_index :
            player = user_exists(db, team['members'][p_index])


        team_string += '**['+str(p_index+1)+']** '
        if player:
            team_string += player['battle_tag']+'\n'
        else:
            team_string += '*EMPTY*\n'
        p_index += 1
        

    return team_string


async def team_details_hanlder(db, message):
    
    word_list = message.content.split(' ')
    if len(word_list) > 1:

        team_name = make_string_from_word_list(word_list, 1)
        existing_team = await get_team_by_name(db, team_name)
        if existing_team:
            team_details = make_details_from_team(db, existing_team)
            await message.channel.send(team_details)
        else:
            await message.channel.send('There is no team with the name "'+team_name+'"')

    else:
        await invalid_number_of_params(message)