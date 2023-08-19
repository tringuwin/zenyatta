
import constants

async def get_guild(client):

    guild = client.get_guild(constants.GUILD_ID)
    return guild

async def give_role_to_user(client, discord_user, role_id):
    
    guild = get_guild(client)
    role = guild.get_role(role_id)

    await discord_user.add_roles(role)