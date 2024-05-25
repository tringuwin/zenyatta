

from discord_actions import get_guild
from user import user_exists
import discord
import constants

async def contact_member_to_reg(member, client):

    try:
        await member.send("Please register before entering XP Battles. To register, go to this channel ( https://discord.com/channels/1130553449491210442/1130553489106411591 ) and use this command to register: **!battle YourBattleTagHere#1234**")
    except discord.Forbidden:
        guild = await get_guild(client)
        chat_channel = guild.get_channel(constants.CHAT_CHANNEL)
        await chat_channel.send(member.mention+" Please register before entering XP Battles. To register, go to this channel ( https://discord.com/channels/1130553449491210442/1130553489106411591 ) and use this command to register: **!battle YourBattleTagHere#1234** (I tried to DM you but your privacy settings did not allow me to)")

async def add_to_battle(db, member, battle_info, client):

    if not battle_info['reg_open']:
        return
    
    sign_ups = battle_info['sign_ups']
    if member.id in sign_ups:
        return
    
    user = user_exists(db, member.id)
    if user:
        await contact_member_to_reg(member, client)
        return
    
    battle_info['sign_ups'].append(member.id)
    constants_db = db['constants']
    constants_db.update_one({"name": "battle"}, {"$set": {"value": battle_info}})

    


    