

from command_handlers.battle import battle_link


async def force_battle_handler(db, message, client):
    
    parts = message.content.split()
    battle_tag = parts[2]
    if battle_tag.lower == "@everyone" or "@here":
        await message.channel.send('User not found.')
        return
    user = message.mentions[0]

    await battle_link(db, message, client, user, battle_tag)