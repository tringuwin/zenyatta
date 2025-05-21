

from common_messages import not_registered_response
from helpers import generic_find_user, update_token_tracker, valid_number_of_params
from user.user import get_league_team, get_lvl_info, get_user_lootboxes, user_exists


async def change_tokens(db, user, num, source='unknown'):

    users = db['users']
    
    if "tokens" in user:
        new_tokens = user['tokens'] + num
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": new_tokens}})
    else:
        users.update_one({"discord_id": user['discord_id']}, {"$set": {"tokens": num}})

    update_token_tracker(db, source, num)

async def give_tokens_command(client, db, user_id, num, message):

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('Could not find user with that ID')
        return
    
    await change_tokens(db, user, num, 'admin-give-tokens')
    await message.channel.send('Tokens given')


async def sell_pickaxe_for_tokens(db, message):

    user = user_exists(db, int(message.author.id))

    if not user:
        await not_registered_response(message)

    if 'pickaxes' in user and user['pickaxes'] > 0:
        await change_pickaxes(db, user, -1)
        await change_tokens(db, user, 15, 'sell-pickaxe')
        await message.channel.send('You sold 1 Pickaxe for **15 Tokens!**')
    else:
        await message.channel.send('You do not have any pickaxes to sell.')



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




async def change_xp(db, user, num, client):

    users = db['users']

    league_team = get_league_team(user)
    if league_team != 'None':

        constants_db = db['constants']

        league_xp_obj = constants_db.find_one({'name': 'league_xp'})
        league_xp = league_xp_obj['value']
        if league_team in league_xp:
            league_xp[league_team] += num
            constants_db.update_one({"name": 'league_xp'}, {"$set": {"value": league_xp}})

        league_xp_total_obj = constants_db.find_one({'name': 'league_xp_total'})
        league_xp_total = league_xp_total_obj['value']
        if league_team in league_xp_total:
            league_xp_total[league_team] += num
            constants_db.update_one({"name": 'league_xp_total'}, {"$set": {"value": league_xp_total}})
    
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