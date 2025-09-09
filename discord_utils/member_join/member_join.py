import constants
from safe_send import safe_dm
from user.user import user_exists

async def member_joined(member, db, client):

    guild = client.get_guild(constants.GUILD_ID)
    role = guild.get_role(constants.MEMBER_ROLE_ID)
    server_notifs = guild.get_role(constants.SERVER_NOTIFS_ROLE)
    tourney_notifs = guild.get_role(constants.TOURNEY_NOTIFS_ROLE)
    twitch_notifs = guild.get_role(constants.TWITCH_NOTIFS_ROLE)
    league_notifs = guild.get_role(constants.LEAGUE_NOTIFS_ROLE)

    if role is not None:

        registered_user = user_exists(db, member.id)
        if registered_user:
            registered_role = guild.get_role(constants.REGISTERED_ROLE)
            image_perm_role = guild.get_role(constants.IMAGE_PERMS_ROLE)
            await member.add_roles(role, server_notifs, tourney_notifs, twitch_notifs, league_notifs, registered_role, image_perm_role)
        else:
            await member.add_roles(role, server_notifs, tourney_notifs, twitch_notifs, league_notifs)

    try:

        default_msg = "Welcome to the Spicy Esports Discord Server! I'm *Scovi*, the server's helper bot. "
        default_msg += '\n\nIf you are interested in joining a team, you can make a post in the team up channel with some info about yourself and what you are looking for in a team:'
        default_msg += '\n\nOverwatch Team Up Channel: https://discord.com/channels/1130553449491210442/1171266378813149244'
        default_msg += '\nMarvel Rivals Team Up Channel: https://discord.com/channels/1130553449491210442/1316625582825541644'
        default_msg += '\n\nIf you cannot see the channels above, make sure sure to select your game roles here: https://discord.com/channels/1130553449491210442/1316612922985811968'
        default_msg += '\n\nThank you for joining! If you have any questions, feel free to ask our friendly staff here: https://discord.com/channels/1130553449491210442/1202441473027477504'

        await safe_dm(member, default_msg)
    except Exception:
        print('Could not DM user.')