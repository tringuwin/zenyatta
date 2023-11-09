
from helpers import make_string_from_word_list
from user import user_exists


async def set_league_team_handler(db, message):

    params = message.content.split()

    user_id = int(params[1])
    team_name = make_string_from_word_list(params, 2)

    user = user_exists(db, user_id)
    if not user:
        await message.channel.send('User not found')
        return
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"league_team": team_name}})

    await message.channel.send('League team updated')

