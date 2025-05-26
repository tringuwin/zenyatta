import discord #im genuinely unsure if this is needed or not for add_roles to work
from discord_actions import get_guild, get_role_by_id
from api import get_member

async def league_admin_role_fix_handler(db, message, client):
        admin_role_id = 1353487134895378582
        admin_role = await get_role_by_id(client, admin_role_id)

        guild = await get_guild(client)

        league_teams = db['rivals_leagueteams']
        all_teams = league_teams.find()
        for team in all_teams:
            members = team['members']
            for member in members:
                if member['is_admin']:
                    member_id = member['discord_id']
                    member_obj = get_member(guild, member_id, 'league_admin_role_fix')
                    await member_obj.add_roles(admin_role)

        await message.channel.send('done')