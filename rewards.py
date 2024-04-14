

from api import give_role, remove_role
from common_messages import not_registered_response
from discord_actions import get_guild, get_member_by_username, get_user_from_guild
from helpers import can_be_int, generic_find_user
from user import get_lvl_info, get_user_lootboxes, user_exists
import constants


async def change_tokens(db, user, num):

    users = db['users']
    
    if "tokens" in user:
        new_tokens = user['tokens'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": new_tokens}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": num}})

async def change_pp(db, user, num):

    users = db['users']
    
    if "poke_points" in user:
        new_points = user['poke_points'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_points": new_points}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"poke_points": num}})


async def give_tokens_command(client, db, user_id, num, message):

    user = None
    if can_be_int(user_id):
        user = user_exists(db, int(user_id))
    if user:
        await change_tokens(db, user, num)
        await message.channel.send('Tokens given')
    else:
        member = await get_member_by_username(client, user_id)
        user = None
        if member:
            user = user_exists(db, member.id)
        if user:
            await change_tokens(db, user, num)
            await message.channel.send('Tokens given')
        else:
            await message.channel.send('Could not find user with that ID')

async def change_passes(db, user, num):

    users = db['users']

    if "passes" in user:
        new_passes = user['passes'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": new_passes}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"passes": num}})


async def give_passes_command(client, db, user_id, num, message):

    user = None
    if can_be_int(user_id):
        user = user_exists(db, int(user_id))
    if user:
        await change_passes(db, user, num)
        await message.channel.send('Passes given')
    else:
        member = await get_member_by_username(client, user_id)
        user = None
        if member:
            user = user_exists(db, member.id)
        if user:
            await change_passes(db, user, num)
            await message.channel.send('Passes given')
        else:
            await message.channel.send('Could not find user with that ID')

async def sell_pass_for_tokens(db, message):

    user = user_exists(db, int(message.author.id))

    if not user:
        await not_registered_response(message)

    if 'passes' in user and user['passes'] > 0:
        await change_passes(db, user, -1)
        await change_tokens(db, user, 10)
        await message.channel.send('You sold 1 Priority Pass for **10 Tokens!**')
    else:
        await message.channel.send('You do not have any priority passes to sell.')

        

async def sell_pickaxe_for_tokens(db, message):

    user = user_exists(db, int(message.author.id))

    if not user:
        await not_registered_response(message)

    if 'pickaxes' in user and user['pickaxes'] > 0:
        await change_pickaxes(db, user, -1)
        await change_tokens(db, user, 15)
        await message.channel.send('You sold 1 Pickaxe for **15 Tokens!**')
    else:
        await message.channel.send('You do not have any pickaxes to sell.')


async def change_eggs(db, user, num):

    users = db['users']
    
    if "eggs" in user:
        new_eggs = user['eggs'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"eggs": new_eggs}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"eggs": num}})


async def give_eggs_command(db, user_id, num, message):

    user = user_exists(db, int(user_id))

    if user:
        await change_eggs(db, user, num)

        await message.channel.send('Eggs given')
    else:
        await message.channel.send('Could not find user with that ID')

async def give_pickaxes_command(client, db, user_id, num, message):

    user = await generic_find_user(client, db, user_id)

    if user:
        await change_pickaxes(db, user, num)

        await message.channel.send('Pickaxes given')
    else:
        await message.channel.send('Could not find user with that ID')


async def give_packs_command(client, db, user_id, num, message):

    user = await generic_find_user(client, db, user_id)

    if user:
        await change_packs(db, user, num)

        await message.channel.send('Packs given')
    else:
        await message.channel.send('Could not find user with that ID')

async def level_up(user, orig_level, new_level, client, db):

    user_boxes = get_user_lootboxes(user)

    move_up = orig_level + 1
    while move_up <= new_level:
        user_boxes.append(move_up)
        move_up += 1
    
    users = db['users']
    users.update_one({"discord_id": user['discord_id']}, {"$set": {"lootboxes": user_boxes}})

    member = await get_user_from_guild(client, user['discord_id'])
    if member:

        guild = await get_guild(client)

        adjusted_orig_level = orig_level - 1
        orig_level_id = constants.LEVEL_ROLE_IDS[adjusted_orig_level]
        orig_level_role = guild.get_role(orig_level_id)

        adjusted_new_level = new_level - 1
        new_level_id = constants.LEVEL_ROLE_IDS[adjusted_new_level]
        new_level_role = guild.get_role(new_level_id)

        await give_role(member, new_level_role, 'Level Up')
        await remove_role(member, orig_level_role, 'Level Up')




async def change_xp(db, user, num, client):

    users = db['users']
    
    level, xp = get_lvl_info(user)

    orig_level = level
    xp += num
    xp_needed_for_level_up = level * 100
    while xp >= xp_needed_for_level_up:
        level += 1
        xp -= xp_needed_for_level_up
        xp_needed_for_level_up = level * 100

    users.update_one({"discord_id": user['discord_id']}, {"$set": {"xp": xp, "level": level}})

    if orig_level != level:
        await level_up(user, orig_level, level, client, db)


async def change_pickaxes(db, user, num):

    users = db['users']
    
    if "pickaxes" in user:
        new_pickaxes = user['pickaxes'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"pickaxes": new_pickaxes}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"pickaxes": num}})


async def change_packs(db, user, num):

    users = db['users']
    
    if "packs" in user:
        new_packs = user['packs'] + num
        final_packs = round(new_packs, 2)
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"packs": final_packs}})
    else:
        final_packs = round(num, 2)
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"packs": num}})