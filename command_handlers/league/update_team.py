
from discord_actions import get_guild
from league import update_team_info
import discord

from league_helpers import get_league_teams_collection
from user import user_exists


async def update_team(db, team_name, client, context):

    guild = await get_guild(client)
    league_teams = get_league_teams_collection(db, context)
    team_object = league_teams.find_one({'team_name': team_name})

    league_team_field = 'league_team' if context == 'OW' else 'rivals_league_team'

    final_team_members = []
    ids_to_remove_team_from = []
    for member in team_object['members']:
        try:
            guild_member = await guild.fetch_member(member['discord_id'])
        except discord.NotFound:
            guild_member = None
            ids_to_remove_team_from.append(member['discord_id'])
        if guild_member:
            final_team_members.append(member)

    league_teams.update_one({'team_name': team_name}, {"$set": {"members": final_team_members}})

    users = db['users']
    for user_id in ids_to_remove_team_from:
        user = user_exists(db, user_id)
        if user:
            users.update_one({"discord_id": user_id}, {"$set": {league_team_field: 'None'}})

    team_object['members'] = final_team_members
    await update_team_info(client, team_object, db, context)



async def update_team_handler(db, message, client, context):

    team_name = message.content.split()[1]

    await update_team(db, team_name, client, context)

    await message.channel.send('Team details updated.')