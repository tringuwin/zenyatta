from user.user import user_exists, get_lvl_info
from api import send_msg


async def give_all_boxes_hander(db, message, client):
        users = db['users']

        for member in client.get_all_members():
            user = user_exists(db, member.id)
            if not user:
                continue
            user_boxes = []
            level, _ = get_lvl_info(user)
            increase_int = 2
            while level >= increase_int:
                user_boxes.append(increase_int)
                increase_int += 1

            users.update_one({"discord_id": user['discord_id']}, {"$set": {"lootboxes": user_boxes}})

        await send_msg(message.channel, 'boxes given', '!giveallboxes')    