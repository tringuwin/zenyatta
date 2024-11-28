

from command_handlers.bets.finish_bet import finish_bet
from common_messages import invalid_number_of_params
from helpers import can_be_int, get_constant_value, valid_number_of_params


def calculate_team_points(team_data):

    win_total = team_data['wins'] * 10
    map_total = team_data['map_wins'] - team_data['map_losses']
    e_sub_total = team_data['esubs'] * -1

    return win_total + map_total + e_sub_total



async def match_end_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 5)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    win_score = params[2]
    lose_score = params[4]

    if not can_be_int(win_score):
        await message.channel.send(win_score+' is not a valid number.')
        return
    if not can_be_int(lose_score):
        await message.channel.send(lose_score+' is not a valid number.')
        return
    
    win_score = int(win_score)
    lose_score = int(lose_score)

    win_team_name = params[1]
    lose_team_name = params[3]

    win_team_name_lower = win_team_name.lower()
    lose_team_name_lower = lose_team_name.lower()
    league_teams = db['leagueteams']

    win_team = league_teams.find_one({'name_lower': win_team_name_lower})
    if not win_team:
        await message.channel.send(win_team_name+' is not a valid team name')
        return
    lose_team = league_teams.find_one({'name_lower': lose_team_name_lower})
    if not lose_team:
        await message.channel.send(lose_team_name+' is not a valid team name')
        return
    
    win_team_real_name = win_team['team_name']
    lose_team_real_name = lose_team['team_name']

    league_season = get_constant_value(db, 'league_season')
    
    standings = db['standings']
    standings_obj = standings.find_one({'season': league_season})

    standings_obj['teams'][win_team_real_name]['wins'] += 1
    standings_obj['teams'][win_team_real_name]['map_wins'] += win_score
    standings_obj['teams'][win_team_real_name]['map_losses'] += lose_score

    standings_obj['teams'][lose_team_real_name]['losses'] += 1
    standings_obj['teams'][lose_team_real_name]['map_wins'] += lose_score
    standings_obj['teams'][lose_team_real_name]['map_losses'] += win_score

    winner_points = calculate_team_points(standings_obj['teams'][win_team_real_name])
    loser_points = calculate_team_points(standings_obj['teams'][lose_team_real_name])

    standings_obj['teams'][win_team_real_name]['points'] = winner_points
    standings_obj['teams'][lose_team_real_name]['points'] = loser_points

    standings.update_one({"season": league_season}, {"$set": {"teams": standings_obj['teams']}})

    # check for bets too

    bets = db['bets']
    team_won = 0
    team_loss = 0
    match_bet_valid = False

    valid_bet = bets.find_one({'team_1': win_team_real_name, 'team_2': lose_team_real_name})
    if valid_bet:
        team_won = 1
        team_loss = 2
        match_bet_valid = True
    else:
        valid_bet = bets.find_one({'team_2': win_team_real_name, 'team_1': lose_team_real_name})

        if valid_bet:
            team_won = 2
            team_loss = 1
            match_bet_valid = True
        else:
            await message.channel.send('Could not find the bet for this matchup.')

    if match_bet_valid:
        await finish_bet(db, message, client, valid_bet, str(team_won), str(team_loss))

    await message.channel.send('match info recorded')


async def team_e_subs(db, message):

    valid_params, params = valid_number_of_params(message, 3)

    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    team_name = params[1]
    esub_num = params[2]

    if not can_be_int(esub_num):
        await message.channel.send(esub_num+' is not a number')
        return
    esub_num = int(esub_num)
    
    league_teams = db['leagueteams']
    league_team = league_teams.find_one({'name_lower': team_name.lower()})
    real_team_name = league_team['team_name']

    if not league_team:
        await message.channel.send('Could not find league team.')
        return
    
    league_season = get_constant_value(db, 'league_season')
    
    standings = db['standings']
    standings_obj = standings.find_one({'season': league_season})

    standings_obj['teams'][real_team_name]['esubs'] += esub_num

    team_points = calculate_team_points(standings_obj['teams'][real_team_name])
    standings_obj['teams'][real_team_name]['points'] = team_points

    standings.update_one({"season": league_season}, {"$set": {"teams": standings_obj['teams']}})

    await message.channel.send('updated esubs for team')

    


