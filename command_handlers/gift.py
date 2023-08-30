from rewards import change_passes, change_tokens
from time_helpers import get_current_time, long_enough_for_gift, time_to_gift
from user import user_exists
import random


async def process_gift(db, current_time, existing_user, message):
    users = db['users']
    users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"last_gift": current_time, "gift_notify": True}})
    general_info = '\n*Come back in 8 hours for another gift!*'

    prize_index = random.randint(1, 100)
    if prize_index == 1:
        await change_tokens(db, existing_user, 100)
        await message.channel.send(message.author.mention+" 🪙 **YOU FOUND 100 TOKENS!!** 🪙"+general_info)
    elif prize_index <= 10:
        await change_passes(db, existing_user, 1)
        await message.channel.send(message.author.mention+" 🎟️ You found a **Priority Pass!** 🎟️"+general_info)
    else:
        tokens = random.randint(2, 5)
        await change_tokens(db, existing_user, tokens)
        await message.channel.send(message.author.mention+" 🪙 You found **"+ str(tokens)+" Tokens** 🪙"+general_info)



async def gift_handler(db, message):

    existing_user = user_exists(db, message.author.id)
    if not existing_user:
        await message.channel.send(message.author.mention+" It looks like you're not registered yet. Please register first!")
        return

    if 'last_gift' in existing_user:
        last_gift_time = existing_user['last_gift']
        long_enough, diff_in_time = long_enough_for_gift(last_gift_time)
       
        if long_enough:
            current_time = get_current_time()
            await process_gift(db, current_time, existing_user, message)
        else:
            await message.channel.send(message.author.mention+" Your gift is not ready yet. Next gift in **"+time_to_gift(diff_in_time)+"**")

    else:
        await process_gift(db, current_time, existing_user, message)

        