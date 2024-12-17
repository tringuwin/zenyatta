import constants
import copy

async def create_new_user(db, user_id, message, rivals_username):
    
    users = db['users']

    username_lower = rivals_username.lower()

    new_user = copy.deepcopy(constants.DEFAULT_BLANK_USER)
    new_user["rivals_username"] = rivals_username
    new_user["rivals_username_lower"] = username_lower
    new_user["discord_id"] = user_id

    users.insert_one(new_user)

    await message.channel.send("You've successfully added your Marvel Rivals username to your discord account.")