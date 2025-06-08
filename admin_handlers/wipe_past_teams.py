

from context.context_helpers import get_teams_joined_this_season_constant

async def wipe_past_teams(db, message, context):
    
    teams_joined_var = get_teams_joined_this_season_constant(context)

    users = db['users']
    all_users = list(users.find())

    users_cleared = 0
    for user in all_users:
        if teams_joined_var in user:
            users.update_one({'discord_id': user['discord_id']}, {'$set': {teams_joined_var: []}})
            users_cleared += 1

    await message.channel.send(f'Wiped past teams for {users_cleared} users in context {context}.')