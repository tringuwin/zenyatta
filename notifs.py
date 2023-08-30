from discord_actions import get_guild, get_role_by_id
import constants
from user import user_exists

async def handle_notifs(db, client):
    
    guild = await get_guild(client)

    gift_role = await get_role_by_id(client, constants.GIFT_ROLE_ID)

    have_gift_notifs = []
    for member in guild.members:
        if gift_role in member.roles:
            have_gift_notifs.append(member)

    for member in have_gift_notifs:
        user = user_exists(db, member.id)
        if not user:
            continue
        
        
