



from command_handlers.league.match_end import calculate_team_points


def apply_match_results_to_standings(standings_teams, match):

    team1 = match['team1']
    team2 = match['team2']

    team1_score = match['team1_score']
    team2_score = match['team2_score']

    winning_team = match['winning_team']

    if winning_team == 0:
        return standings_teams
    
    winning_team_name = team1 if winning_team == 1 else team2
    losing_team_name = team1 if winning_team == 2 else team2

    standings_teams[winning_team_name]['wins'] += 1
    standings_teams[losing_team_name]['losses'] += 1

    standings_teams[team1]['map_wins'] += team1_score
    standings_teams[team1]['map_losses'] += team2_score
    standings_teams[team2]['map_wins'] += team2_score
    standings_teams[team2]['map_losses'] += team1_score

    standings_teams[team1]['points'] = calculate_team_points(standings_teams[team1])
    standings_teams[team2]['points'] = calculate_team_points(standings_teams[team2])

    return standings_teams


def complete_finished_matchups(db, all_matches, context, season):

    matchups = db['matchups']
    matchup_history = db['matchup_history']
    standings = db['standings']

    standings_edited = False
    season_standings = standings.find_one({'context': context, 'season': season})
    standings_teams = season_standings['teams']

    not_completed_matches = []

    for match in all_matches:

        if match['match_over']:
            
            standings_teams = apply_match_results_to_standings(standings_teams, match)
            standings_edited = True

            matchup_history.insert_one(match)
            matchups.delete_one({"_id": match['_id']})
        else:
            not_completed_matches.append(match)


    if standings_edited:
        standings.update_one({'_id': season_standings['_id']}, {"$set": {"teams": standings_teams}})


    return not_completed_matches
