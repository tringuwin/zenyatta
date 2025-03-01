

from common_messages import invalid_number_of_params
from helpers import valid_number_of_params


def find_matchup(matchups, context, winning_team, losing_team):

    matchup_where_winning_team_is_team1 = matchups.find_one({'context': context, 'team1': winning_team, 'team2': losing_team})
    if matchup_where_winning_team_is_team1:
        return matchup_where_winning_team_is_team1
    
    return matchups.find_one({'context': context, 'team1': losing_team, 'team2': winning_team})


def add_teams_to_teams_played(db, matchup):

    schedule_plans = db['schedule_plans']
    schedule_plan = schedule_plans.find_one({'context': matchup['context'], 'season': matchup['season']})

    season_teams = schedule_plan['season_teams']

    for team in season_teams:
        if team['team_name'] == matchup['team1']:
            team['teams_played'].append(matchup['team2'])
        elif team['team_name'] == matchup['team2']:
            team['teams_played'].append(matchup['team1'])

    schedule_plans.update_one({"_id": schedule_plan['_id']}, {"$set": {"season_teams": season_teams}})



async def score_match_handler(db, message, context):

    valid_params, params = valid_number_of_params(message, 7)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    winning_team = params[1]
    winning_team_score = int(params[2])
    winning_team_esubs = int(params[3])

    losing_team = params[4]
    losing_team_score = int(params[5])
    losing_team_esubs = int(params[6])

    matchups = db['matchups']
    matchup = find_matchup(matchups, context, winning_team, losing_team)

    if not matchup:
        await message.channel.send(f'Matchup not found for {winning_team} vs {losing_team} with context {context}.')
        return
    
    add_teams_to_teams_played(db)
    
    winning_team_index = 1 if matchup['team1'] == winning_team else 2
    losing_team_index = 1 if winning_team_index == 2 else 2
    
    matchup_edit = {
        f'team{winning_team_index}_score': winning_team_score,
        f'team{losing_team_index}_score': losing_team_score,
        f'team{winning_team_index}_esubs': winning_team_esubs,
        f'team{losing_team_index}_esubs': losing_team_esubs,
        'match_over': True,
        'winning_team': winning_team_index
    }

    matchups.update_one({"_id": matchup['_id']}, {"$set": matchup_edit})
    await message.channel.send(f'Matchup between {winning_team} and {losing_team} for context {context} has been scored.')
