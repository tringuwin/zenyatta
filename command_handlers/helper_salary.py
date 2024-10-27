

from rewards import change_tokens
from user import user_exists


async def helper_salary_handler(db, message, client):

    user = user_exists(db, message.author.id)

    await change_tokens(db, user, 200, 'helper-salary')

    admin_channel = client.get_channel(1131625086722523297)
    await admin_channel.send(user['battle_tag']+' claimed their helper salary.')

    await message.channel.send('Helper salary claimed!')
