

def create_new_production_crew_member(db, user_id, username):

    production_crew = db['production_crew']

    existing_member = production_crew.find_one({"discord_id": user_id})
    if existing_member:
        return
    
    new_member = {
        "discord_id": user_id,
        "username": username,
        "lower_username": username.lower(),
        "balance": 0.0,
    }

    production_crew.insert_one(new_member)
    