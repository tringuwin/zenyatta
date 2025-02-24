from api import get_member, give_role
import constants
from helpers import valid_number_of_params
from mongo import create_or_update_battle_tag, find_user_with_battle_tag


async def battle_link(db, message, client, user, battle_tag):
    
    if len(battle_tag) > 30:
        await message.channel.send('The battle tag you provided is not valid.')
        return
    
    if not ('#' in battle_tag):
        await message.channel.send("The Battle Tag you provided seems to be missing the # and numbers at the end. Please include that too.")
        return
    
    if battle_tag[0] == '#':
        await message.channel.send('Battle tags cannot start with the "#" character. Please use this format: BattleTag#1234')
        return
        
    lower_tag = battle_tag.lower()
    user_with_battle_tag = find_user_with_battle_tag(db, lower_tag)

    if user_with_battle_tag:
        if user_with_battle_tag['discord_id'] == message.author.id:
            await message.channel.send("You've already linked this battle tag.")
        else:
            await message.channel.send("That Battle Tag has already been connected to a different discord account. Please contact staff if you need help.")
        return
    
    create_or_update_battle_tag(db, battle_tag, lower_tag, user.id)

    guild = client.get_guild(constants.GUILD_ID)
    reg_role = guild.get_role(constants.REGISTERED_ROLE)
    member = get_member(guild, user.id, 'Battle Link')
    if member and reg_role:
        await give_role(member, reg_role, 'Battle Link')

    await message.channel.send("Success! Your Battle Tag has been linked to the Spicy Esports server! (Please note: if you change your Battle Tag please use the !battle command again to update it!)")


async def battle_handler(db, message, client):

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await message.channel.send('This command was not formatted correctly. Please type !battle and then add your Battle Tag.')
        return
    
    await battle_link(db, message, client, message.author, params[1])