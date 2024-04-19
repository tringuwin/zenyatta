
from discord_actions import get_guild
from league import update_team_info
import discord


async def update_team(db, team_name, client, message):

    guild = await get_guild(client)
    league_teams = db['leagueteams']
    team_object = league_teams.find_one({'team_name': team_name})

    if not team_object:
        await message.channel.send('Team not found')
        return
    
    final_team_members = []
    for member in team_object['members']:
        try:
            guild_member = await guild.fetch_member(member['discord_id'])
        except discord.NotFound:
            guild_member = None
        if guild_member:
            final_team_members.append(member)

    league_teams.update_one({'team_name': team_name}, {"$set": {"members": final_team_members}})

    team_object['members'] = final_team_members
    await update_team_info(client, team_object, db)



async def update_team_handler(db, message, client):

    team_name = message.content.split()[1]

    await update_team(db, team_name, client, message)

    await message.channel.send('Team details updated.')