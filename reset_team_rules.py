async def reset_team_rules_handler(db, message):
    users = db['users']
    all_users = users.find()

    for user in all_users:

        changes_made = False
        set_array = {}

        if 'team_swaps' in user:
            changes_made = True
            set_array['team_swaps'] = 3

        if 'user_div' in user:
            changes_made = True
            set_array['user_div'] = 0

        if changes_made:
            users.update_one({'discord_id': user['discord_id']}, {'$set': set_array})