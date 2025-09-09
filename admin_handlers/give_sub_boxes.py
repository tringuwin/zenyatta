
from discord_actions import get_guild, get_role_by_id
import constants
from safe_send import safe_send
from user.user import get_last_sub_box, get_sub_lootboxes, get_user_packs, user_exists
import time

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
                user_boxes = get_sub_lootboxes(user)
                current_time = time.time()
                difference = current_time - last_sub_box
                if difference >= constants.TIME_IN_30_DAYS:
                    boxes_given += 1
                    user_boxes += 1
                    user_packs = get_user_packs(user)
                    users.update_one({"discord_id": user['discord_id']}, {"$set": {"sub_lootboxes": user_boxes, 'last_sub_box': current_time, 'packs': user_packs + 3}})

    await safe_send(message.channel, 'Command complete. '+str(boxes_given)+' total twitch lootboxes given.')