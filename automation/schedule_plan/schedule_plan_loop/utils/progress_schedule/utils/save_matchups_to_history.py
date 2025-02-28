

def save_matchups_to_history(db, all_matches):

    matchups = db['matchups']
    matchup_history = db['matchup_history']

    for match in all_matches:
        matchup_history.insert_one(match)
        matchups.delete_one({"_id": match['_id']})
