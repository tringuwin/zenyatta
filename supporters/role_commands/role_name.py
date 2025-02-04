

from discord_actions import get_guild
from helpers import make_string_from_word_list


async def role_name(client, db, message):

    custom_roles = db['custom_roles']

    user_id = message.author.id
    user_role_obj = custom_roles.find_one({'user_id': user_id})
    if not user_role_obj:

        no_role_message = 'You do not currently have a custom role assigned. You can get a custom role by subscribing to this discord. (Check our server shop for more info)'
        no_role_message +='\n\n*If you subscribed to this discord but do not have a role yet, it can take up to 20 minutes. If it takes longer, please contact staff*'
        await message.reply(no_role_message)
        return
    
    guild = await get_guild(client)

    user_role_id = user_role_obj['role_id']
    user_role = guild.get_role(user_role_id)
    if not user_role:
        raise Exception('Could not find the role for a supporter in the discord server.')
    
    new_role_name = make_string_from_word_list(message.content.split(), 1)
    await user_role.edit(name=new_role_name)
    await message.channel.send('You have changed your custom role name to "'+new_role_name+'"')
    
    
