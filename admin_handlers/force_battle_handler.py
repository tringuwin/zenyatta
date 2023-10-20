

from command_handlers.battle import battle_link


async def force_battle_handler(db, message, client):
    
    parts = message.content.split()
    battle_tag = parts[2]
    user = message.mentions[0]

    await battle_link(db, message, client, user, battle_tag)