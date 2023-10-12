from common_messages import not_registered_response
from discord_actions import get_guild, member_has_role
from rewards import change_passes, change_pickaxes, change_tokens
from time_helpers import get_current_time, long_enough_for_gift, time_to_gift
from user import get_user_gems, user_exists
import random
import constants


async def give_gem(db, message, user, end_string, client):

    random_gem = random.choice(constants.GEM_COLORS)
    user_gems = get_user_gems(user)
    user_gems[random_gem] += 1

    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"gems": user_gems}})

    guild = await get_guild(client)
    gem_emoji_id = constants.COLOR_TO_EMOJI_ID[random_gem]
    gem_emoji = guild.get_emoji(gem_emoji_id)

    await message.channel.send(message.author.mention+" "+str(gem_emoji)+' **You found a '+random_gem+' gem!!** '+str(gem_emoji)+end_string)
    




async def process_gift(db, current_time, existing_user, message, client):

    is_sub = member_has_role(message.author, constants.TWITCH_SUB_ROLE)

    users = db['users']
    users.update_one({"discord_id": existing_user['discord_id']}, {"$set": {"last_gift": current_time, "gift_notify": True}})
    general_info = '\n*Come back in 8 hours for another gift!*'

    prize_index = random.randint(1, 100)
    if is_sub:
        general_info += "\n~ Since you're a Twitch Sub, you get better gift rewards! ~"
        if prize_index <= 3:
            await change_tokens(db, existing_user, 100)
            await message.channel.send(message.author.mention+" 🪙 **YOU FOUND 100 TOKENS!!** 🪙"+general_info)
        elif prize_index <= 9:
            await change_passes(db, existing_user, 1)
            await message.channel.send(message.author.mention+" 🎟️ You found a **Priority Pass!** 🎟️"+general_info)
        elif prize_index <= 20:
            await change_pickaxes(db, existing_user, 1)
            await message.channel.send(message.author.mention+" ⛏️ You found a **Pickaxe!** ⛏️ Use it in the Mineshaft! "+general_info)
        elif prize_index <= 30:
            await give_gem(db, message, existing_user, general_info, client)
        else:
            tokens = random.randint(10, 20)
            await change_tokens(db, existing_user, tokens)
            await message.channel.send(message.author.mention+" 🪙 You found **"+ str(tokens)+" Tokens** 🪙"+general_info)
    else:
        if prize_index == 1:
            await change_tokens(db, existing_user, 100)
            await message.channel.send(message.author.mention+" 🪙 **YOU FOUND 100 TOKENS!!** 🪙"+general_info)
        elif prize_index <= 5:
            await change_passes(db, existing_user, 1)
            await message.channel.send(message.author.mention+" 🎟️ You found a **Priority Pass!** 🎟️"+general_info)
        elif prize_index <= 10:
            await change_pickaxes(db, existing_user, 1)
            await message.channel.send(message.author.mention+" ⛏️ You found a **Pickaxe!** ⛏️ Use it in the Mineshaft! "+general_info)
        elif prize_index <= 15:
            await give_gem(db, message, existing_user, "", client)
        else:
            tokens = random.randint(2, 5)
            await change_tokens(db, existing_user, tokens)
            await message.channel.send(message.author.mention+" 🪙 You found **"+ str(tokens)+" Tokens** 🪙"+general_info)



async def gift_handler(db, message, client, is_admin):

    existing_user = user_exists(db, message.author.id)
    if not existing_user:
        await not_registered_response(message)
        return

    current_time = get_current_time()
    if 'last_gift' in existing_user:
        last_gift_time = existing_user['last_gift']
        long_enough, diff_in_time = long_enough_for_gift(last_gift_time)
       
        if long_enough or is_admin:
            await process_gift(db, current_time, existing_user, message, client)
        else:
            await message.channel.send(message.author.mention+" Your gift is not ready yet. Next gift in **"+time_to_gift(diff_in_time)+"**")

    else:
        await process_gift(db, current_time, existing_user, message, client)

        