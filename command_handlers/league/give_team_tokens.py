
from common_messages import invalid_number_of_params
import constants
from helpers import can_be_int, make_string_from_word_list
import math
from rewards import change_tokens

from user import user_exists

async def give_team_tokens_handler(db, message):

    word_parts = message.content.split()
    if len(word_parts) < 3:
        await invalid_number_of_params(message)
        return
    
    tokens_to_give = word_parts[1]
    if not can_be_int(tokens_to_give):
        await message.channel.send(tokens_to_give+' is not an integer')
        return
    tokens_to_give = int(tokens_to_give)
    
    team_name = make_string_from_word_list(word_parts, 2)
    if not team_name in constants.TEAM_LIST:
        await message.channel.send(team_name+' is not a valid team name')
        return
    
    league_teams = db['leagueteams']
    team_obj = league_teams.find_one({'team_name': team_name})
    if not team_obj:
        await message.channel.send('Internal error: did not find team')
        return
    
    total_team_tpp = 0
    tpp_table = []
    for member in team_obj['members']:
        if member['TPP'] > 0:
            tpp_table.append({
                'discord_id': member['discord_id'],
                'TPP': member['TPP']
            })
            total_team_tpp += member['TPP']

    if total_team_tpp == 0:
        await message.channel.send('Team has no TPP set')
        return
    
    for member in tpp_table:
        member_tpp_percent = float(member['TPP']) / float(total_team_tpp)
        tokens_to_get_raw = float(tokens_to_give) * member_tpp_percent
        final_tokens = math.floor(tokens_to_get_raw)
        user = user_exists(db, member['discord_id'])
        print('giving '+str(final_tokens)+' to '+user['battle_tag'])
        await change_tokens(db, user, final_tokens) 


    await message.channel.send('Done')
    

    



