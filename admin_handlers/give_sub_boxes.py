
from discord_actions import get_guild, get_role_by_id
import constants
from user import get_last_sub_box, user_exists
import time

TIME_IN_30_DAYS = 2592000

async def give_sub_boxes_handler(db, message, client):

    guild = await get_guild(client)
    twitch_sub_role_id = constants.TWITCH_SUB_ROLE
    twitch_sub_role = await get_role_by_id(client, twitch_sub_role_id)

    users = db['users']
    boxes_given = 0

    for member in guild.members:
        if twitch_sub_role in member.roles:
            user = user_exists(db, member.id)
            if user:
                last_sub_box = get_last_sub_box(user)
                current_time = time.time()
                difference = current_time - last_sub_box
                if difference >= TIME_IN_30_DAYS:
                    boxes_given += 1
                    users.update_one({"discord_id": user['discord_id']}, {"$set": {"sub_lootboxes": user['sub_lootboxes']+1, 'last_sub_box': current_time}})

    await message.channel.send('Command complete. '+str(boxes_given)+' total twitch lootboxes given.')