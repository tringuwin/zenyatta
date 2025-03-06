

def get_matchups_for_week(db, context, league_season, league_week):

    matchups = db['matchups']
    return list(matchups.find({'context': context, 'season': league_season, 'week': league_week}))

