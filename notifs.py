from discord_actions import get_guild, get_role_by_id
import constants

async def handle_notifs(db, client):
    
    guild = await get_guild(client)

    gift_role = await get_role_by_id(client, constants.GIFT_ROLE_ID)

    have_gift_notifs = []
    for member in guild.members:
        if gift_role in member.roles:
            have_gift_notifs.append(member)

    print(str(len(have_gift_notifs))+' people have gift notifs')
        
