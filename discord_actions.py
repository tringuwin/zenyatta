
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
    if role:
        await discord_user.add_roles(role)

async def remove_role_from_user(client, discord_user, role_id):

    guild = await get_guild(client)
    role = guild.get_role(role_id)
    if role:
        await discord_user.remove_roles(role)


async def get_user_from_guild(client, user_id):

    guild = await get_guild(client)
    discord_user = None
    try:
        discord_user = await guild.fetch_member(user_id)
        if discord_user:
            return discord_user
    except discord.errors.NotFound:
        return None
    
    return None

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

def member_has_role(member, role_id):

    for role in member.roles:
        if role.id == role_id:
            return True
    
    return False


def is_dm_channel(channel):

    if isinstance(channel, discord.DMChannel):
        return True
    else:
        return False
    

async def get_message_by_channel_and_id(client, channel_id, message_id):

    channel = client.get_channel(channel_id)
    if channel:
        message = await channel.fetch_message(message_id)
        return message

