

from discord_actions import get_guild, get_member_by_id
from helpers import generic_find_user, valid_number_of_params




ALERT_CODE_TO_MESSAGE = {
    'sent1': 'Your $1 Battle Balance from your drop <:spicy_drop:1327677388720701450> has been sent to your account!',
    'friend1': "Hello, for staff to gift you the $1 Battle Balance from your drop <:spicy_drop:1327677388720701450>, You will need to be friends with SpicyRagu's overwatch account for 3 days, due to blizzard's rules. A friend request will be sent to your account now, please accept when you can.",
}


async def drop_alert(client, db, message):

    valid_params, params = valid_number_of_params(message, 3)
    if not valid_params:
        await message.channel.send('Invalid number of params')
        return
    
    user_id = params[1]
    alert_code = params[2]

    user = await generic_find_user(client, db, user_id)
    if not user:
        await message.channel.send('Could not find a matching user.')
        return
    
    guild = await get_guild(client)
    member = await get_member_by_id(guild, user['discord_id'])
    if not member:
        await message.channel.send('Could not find member in the server.')
        return
    
    if not alert_code in ALERT_CODE_TO_MESSAGE:
        await message.channel.send('Invalid alert code.')
        return

    alert_message = ALERT_CODE_TO_MESSAGE[alert_code]
    alert_message += '\n\n*I cannot see responses here. If you need help, please contact staff by making a support ticket.*'

    await member.send(alert_message)