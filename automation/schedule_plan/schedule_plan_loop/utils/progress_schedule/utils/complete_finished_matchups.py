

def complete_finished_matchups(db, all_matches):

    matchups = db['matchups']
    matchup_history = db['matchup_history']

    not_completed_matches = []

    for match in all_matches:

        if match['match_over']:
            matchup_history.insert_one(match)
            matchups.delete_one({"_id": match['_id']})
        else:
            not_completed_matches.append(match)

    return not_completed_matches
