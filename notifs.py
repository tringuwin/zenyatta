import discord
from discord_actions import get_guild, get_role_by_id
import constants
from time_helpers import long_enough_for_gift
from user import get_gift_notify, toggle_off_gift_notify, user_exists


async def contact_member_about_gift(member, bot_channel):
    print('contacting '+member.name)
    try:
        await member.send('Your gift is ready in the Spicy Ragu server! Use the command **!gift** to claim it!')
    except discord.Forbidden:
        print('I could not dm the user')
        await bot_channel.send(member.mention+" Your gift is ready! Use the command **!gift** to claim it! (I tried to DM you first but your privacy settings didn't let me).")
    except Exception as e:
        print(f'an unknown error occurred: {e}')


async def handle_notifs(db, client):
    
    guild = await get_guild(client)

    gift_role = await get_role_by_id(client, constants.GIFT_ROLE_ID)

    have_gift_notifs = []
    for member in guild.members:
        if gift_role in member.roles:
            have_gift_notifs.append(member)

    members_to_contact = []
    for member in have_gift_notifs:
        user = user_exists(db, member.id)
        if not user:
            continue

        print(member.name + ' has gift notify')
        if 'last_gift' in user:
            print(member.name+' has last gift')
            gift_notify = get_gift_notify(user)
            if gift_notify:
                print('gift notify is true')
                last_gift_time = user['last_gift']
                if long_enough_for_gift(last_gift_time):
                    print('We will contact '+member.name)
                    members_to_contact.append(member)

    bot_channel = guild.get_channel(constants.BOT_CHANNEL)
    for member in members_to_contact:
        user = user_exists(db, member.id)
        toggle_off_gift_notify(db, user)
        await contact_member_about_gift(member, bot_channel)



        
