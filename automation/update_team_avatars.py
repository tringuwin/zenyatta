import time
from context.context_helpers import get_league_team_image_update_index, get_league_teams_collection_from_context, get_team_list_from_context
from discord_actions import get_member_by_id
from helpers import get_constant_value, set_constant_value


async def update_team_avatars(guild, db, message, context):

    constant_name = get_league_team_image_update_index(context)
    current_team_index = get_constant_value(db, constant_name)
    team_list = get_team_list_from_context(context)
    team_to_update = team_list[current_team_index]

    league_teams = get_league_teams_collection_from_context(db, context)
    league_team = league_teams.find_one({'team_name': team_to_update})
    if not league_team:
        await message.channel.send('Critical error. Could not find team '+team_to_update)
        return
    
    users = db['users']
    updated = 0
    for member in league_team['members']:

        discord_user = await get_member_by_id(guild, member['discord_id'])
        if discord_user:
            discord_user_avatar = discord_user.display_avatar
            if discord_user_avatar:
                users.update_one({'discord_id': member['discord_id']}, {'$set': {'avatar': discord_user_avatar.url}})
                updated += 1
        
        time.sleep(1)

    await message.channel.send('Updated profile pictures for '+str(updated)+' users on team '+team_to_update)

    new_index = current_team_index + 1
    if new_index >= len(team_list):
        new_index = 0

    set_constant_value(db, constant_name, new_index)



async def update_overwatch_team_avatars(guild, db, message):

    await update_team_avatars(guild, db, message, 'OW')


async def update_rivals_team_avatars(guild, db, message):

    await update_team_avatars(guild, db, message, 'MR')


async def update_valorant_team_avatars(guild, db, message):
    
    await update_team_avatars(guild, db, message, 'VL')