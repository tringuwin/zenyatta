
import discord
from discord_actions import get_guild
from helpers import is_valid_hex_code, make_string_from_word_list, valid_number_of_params


async def role_color(client, db, message):

    custom_roles = db['custom_roles']

    user_id = message.author.id
    user_role_obj = custom_roles.find_one({'user_id': user_id})
    if not user_role_obj:

        no_role_message = 'You do not currently have a custom role assigned. You can get a custom role by subscribing to this discord. (Check our server shop for more info)'
        no_role_message +='\n\n*If you subscribed to this discord but do not have a role yet, it can take up to 20 minutes. If it takes longer, please contact staff*'
        await message.reply(no_role_message)
        return
    
    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await message.channel.send('Command not formatted correctly. Use a hex code at the color. For example: **!rolecolor #FF0000**')
        return
    
    color_raw = params[1]
    if not is_valid_hex_code(color_raw):
        await message.channel.send(color_raw+' is not a valid hex code.')
        return
    discord_color = discord.Colour.from_str(color_raw)
    
    guild = await get_guild(client)

    user_role_id = user_role_obj['role_id']
    user_role = guild.get_role(user_role_id)
    if not user_role:
        raise Exception('Could not find the role for a supporter in the discord server.')


    await user_role.edit(color=discord_color)
    await message.channel.send('You have changed your custom role color to "'+color_raw+'"')
    
    
