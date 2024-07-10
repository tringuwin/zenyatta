
from league import validate_admin


async def set_lineup_handler(db, message):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    await message.author.send('Hey lol')