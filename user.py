def user_exists(db, discord_id):
    
    users = db['users']

    search_query = {"discord_id": int(discord_id)}

    return users.find_one(search_query)


def add_team_to_user(db, user, team_name):

    users = db['users']

    if not ('teams' in user):
        user['teams'] = []

    user['teams'].append(team_name)
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"teams": user['teams']}})