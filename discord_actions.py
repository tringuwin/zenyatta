
import constants
import discord

async def get_guild(client):

    guild = client.get_guild(constants.GUILD_ID)
    return guild

async def get_role_by_id(client, role_id):

    guild = await get_guild(client)
    role = guild.get_role(role_id)
    return role

async def give_role_to_user(client, discord_user, role_id):
    
    guild = await get_guild(client)
    role = guild.get_role(role_id)

    await discord_user.add_roles(role)


async def get_user_from_guild(client, user_id):

    guild = await get_guild(client)
    discord_user = await guild.fetch_member(user_id)

    return discord_user

async def get_member_by_username(client, username):

    for member in client.get_all_members():

        disc = member.discriminator
        final_name = member.name
        if disc != '0':
            final_name = final_name+"#"+disc

        if username == final_name:
            return member

    return None

async def get_member_by_id(guild, id):

    return await guild.fetch_member(id)

def is_dm_channel(channel):

    if isinstance(channel, discord.DMChannel):
        return True
    else:
        return False