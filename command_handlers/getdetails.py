
from common_messages import invalid_number_of_params
from discord_actions import get_member_by_username
from helpers import valid_number_of_params
from user import get_user_by_tag, get_user_passes, get_user_tokens, user_exists


async def get_details_handler(db, message, client, is_admin):
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return

    input_string = params[1]

    user = get_user_by_tag(db, input_string.lower())
    if not user:

        member = await get_member_by_username(client, input_string)
        if not member:
            await message.channel.send('There is no member with that username.')
            return

        user = user_exists(db, member.id)
        if not user:
            await message.channel.send('That user is not registered yet.')
            return

    valid_command = is_admin or (user['discord_id'] == message.author.id)
    if not valid_command:
        await message.channel.send('You can only use this command to get your own details.')
        return

    final_string = 'User ID: '+str(user.id)+"\nBattle Tag: "+user['battle_tag']
    final_string += '\nTokens: '+str(get_user_tokens(user))+'\n'+'Passes: '+str(get_user_passes(user))
    await message.channel.send(final_string)
   

        