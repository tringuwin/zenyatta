import time

from discord_actions import get_member_by_id
from safe_send import safe_send

async def update_top_subs_avatars(guild, db, message):

    users = db['users']

    all_users = users.find()

    filtered_users = [user for user in all_users if (('subcount' in user) and ('twitch' in user))]

    final_users = []
    for user in filtered_users:
        final_users.append({
            'user_id': user['discord_id'],
            'subcount': user['subcount'],
        })

    sorted_users = sorted(final_users, key=lambda x: x["subcount"], reverse=True)
    top_20_array = sorted_users[:20]

    updated = 0
    for sorted_user in top_20_array:

        user = users.find_one({'discord_id': sorted_user['user_id']})
        if user:
            discord_user = await get_member_by_id(guild, sorted_user['user_id'])
            if discord_user:
                discord_user_avatar = discord_user.display_avatar
                if discord_user_avatar:
                    users.update_one({'discord_id': sorted_user['user_id']}, {'$set': {'avatar': discord_user_avatar.url}})
                    updated += 1


        time.sleep(1)

    await safe_send(message.channel, 'Updated profile pictures for '+str(updated)+' users.')