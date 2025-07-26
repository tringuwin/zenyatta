

from command_handlers.league.match_end import calculate_team_points


def make_blank_standings(teams):

    all_teams = {}

    for team in teams:
        team_name = team['team_name']

        all_teams[team_name] = {
            'team_name': team_name,
            'wins': 0,
            'losses': 0,
            'map_wins': 0,
            'map_losses': 0,
            'forfeits': 0,
            'points': 0,
        }

    return all_teams


def apply_matchup_to_standings(standings, matchup):

    team1 = matchup['team1']
    team2 = matchup['team2']

    team1_score = matchup['team1_score']
    team2_score = matchup['team2_score']

    winning_team_index = matchup['winning_team']

    winning_team_name = team1 if winning_team_index == 1 else team2
    losing_team_name = team2 if winning_team_index == 1 else team1
    winning_team_score = team1_score if winning_team_index == 1 else team2_score
    losing_team_score = team2_score if winning_team_index == 1 else team1_score

    standings[winning_team_name]['wins'] += 1
    standings[winning_team_name]['map_wins'] += winning_team_score
    standings[winning_team_name]['map_losses'] += losing_team_score

    standings[losing_team_name]['losses'] += 1
    standings[losing_team_name]['map_wins'] += losing_team_score
    standings[losing_team_name]['map_losses'] += winning_team_score

    return standings


async def fix_standings_handler(db, message, context):

    schedule_plans = db['schedule_plans']

    schedule_plan = schedule_plans.find_one({'context': context, 'status': 'IN PROGRESS'})
    if not schedule_plan:
        await message.channel.send(f'No in progress schedule found for the context {context}')
        return
    season_number = schedule_plan['season']
    
    standings = db['standings']
    season_standings = standings.find_one({'context': context, 'season': season_number})
    if not season_standings:
        await message.channel.send(f'No standings found for the context {context} and season {season_number}')
        return
    
    new_standings = make_blank_standings(schedule_plan['season_teams'])

    matchup_history = db['matchup_history']
    all_matchups_in_season = list(matchup_history.find({'context': context, 'season': season_number}))

    for matchup in all_matchups_in_season:
        new_standings = apply_matchup_to_standings(new_standings, matchup)

    # apply forfeits to standings
    forfeits_dict = season_standings.get('forfeits', {})

    # Calculate points based on wins and losses
    for team_name in new_standings:
        
        team = new_standings[team_name]
        base_team_points = calculate_team_points(team)

        num_forfeits = forfeits_dict.get(team_name, 0)
        team['forfeits'] = num_forfeits
        team['points'] = base_team_points - (num_forfeits * 5)

    print('new standings', new_standings)

    standings.update_one({'context': context, 'season': season_number}, {'$set': {'teams': new_standings}})

    await message.channel.send(f'Fixed standings for {context} season {season_number}')