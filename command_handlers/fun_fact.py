
import time
from common_messages import not_registered_response
from user import user_exists

async def fun_fact_handler(db, message):
    fun_fact = message.content[len("!funfact "):].strip()

    existing_user = user_exists(db, message.author.id)

    if not existing_user:
        await not_registered_response(message)
        return

    users = db['users']

    users.update_one({'discord_id': existing_user['discord_id']}, {"$set": {"fun_fact": fun_fact}})
    await message.delete()
    del_msg = await message.channel.send('Your fun fact has been added!')
    time.sleep(5)
    await del_msg.delete()

