
def get_all_matchups(db, league_context, season, week):

    matchups_collection = db['matchups']

    matchups = list(matchups_collection.find({
        'context': league_context,
        'season': season,
        'week': week
    }))

    return matchups