from discord_actions import get_guild, get_role_by_id
import constants
import time

from user import get_last_sac, user_exists

TIME_IN_30_DAYS = 2592000

async def prune_sac_handler(db, message, client):

    guild = await get_guild(client)
    sac_role_id = constants.SAC_ROLE
    sac_role = await get_role_by_id(client, sac_role_id)

    roles_removed = 0
    current_time = time.time()

    for member in guild.members:
        if sac_role in member.roles:
            user = user_exists(db, member.id)
            if user:
                last_sac = get_last_sac(user)
                difference = current_time - last_sac
                if difference >= TIME_IN_30_DAYS:
                    await member.remove_roles(sac_role)
                    roles_removed += 1

    await message.channel.send('Command complete. '+str(roles_removed)+' total roles removed.')