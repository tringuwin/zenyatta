
from discord_actions import get_guild
import constants


async def start_battle_handler(db, message, client):

    constants_db = db['constants']
    battle_obj = constants_db.find_one({'name': 'battle'})
    battle_info = battle_obj['value']

    if battle_info['battle_on']:
        await message.channel.send('There is already an XP Battle in progress. Please end that one first.')
        return
    
    guild = await get_guild(client)
    xp_channel = guild.get_channel(constants.XP_BATTLE_CHANNEL)

    xp_message = await xp_channel.send('A NEW XP BATTLE IS STARTING NOW! REACT WITH ⚔️ FOR A CHANCE TO JOIN!')
    await xp_message.add_reaction('⚔️')
    
    battle_info['battle_on'] = True
    battle_info['reg_open'] = True
    battle_info['reg_message_id'] = xp_message.id
    battle_info['sign_ups'] = []
    battle_info['current_players'] = []
    battle_info['current_teams'] = {'overwatch': [], 'talon': []}
    constants_db.update_one({"name": "battle"}, {"$set": {"value": battle_info}})

    await message.channel.send('Battle Sign-Up Started')