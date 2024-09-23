

from common_messages import invalid_number_of_params
from helpers import can_be_int, valid_number_of_params


async def match_end_handler(db, message):

    pass

    # valid_params, params = valid_number_of_params(message, 5)

    # if not valid_params:
    #     await invalid_number_of_params(message)
    #     return
    
    # win_score = params[3]
    # lose_score = params[5]

    # if not can_be_int(win_score):
    #     await message.channel.send(win_score+' is not a valid number.')
    #     return
    # if not can_be_int(lose_score):
    #     await message.channel.send(lose_score+' is not a valid number.')
    #     return
    
    # win_score = int(win_score)
    # lose_score = int(lose_score)


    # win_team_name = params[2]
    # lose_team_name = params[4]

    # team_name_lower = params[1].lower()
    # league_teams = db['leagueteams']
    # my_team = league_teams.find_one({'name_lower': team_name_lower})
    # if not my_team:
    #     await message.channel.send(params[1]+' is not a valid team name')
    #     return
    # team_name = my_team['team_name']
    
    # num_to_add = params[2]
    # if not can_be_int(num_to_add):
    #     await message.channel.send(params[2]+' is not a number')
    #     return
    # num_to_add = int(num_to_add)

    # league_season = get_constant_value(db, 'league_season')
    
    # standings = db['standings']
    # standings_obj = standings.find_one({'season': league_season})
    # standings_obj['teams'][team_name][2] += num_to_add

    # standings.update_one({"season": league_season}, {"$set": {"teams": standings_obj['teams']}})

    # await message.channel.send('team maps changed')