
from common_messages import not_registered_response
from user import get_sub_lootboxes, get_user_lootboxes, user_exists


async def lootboxes_handler(db, message):

    user = user_exists(db, message.author.id)
    if not user:
        await not_registered_response(message)
        return
    
    user_lootboxes = get_user_lootboxes(user)
    twitch_lootboxes = get_sub_lootboxes(user)

    if len(user_lootboxes) == 0 and twitch_lootboxes == 0:
        await message.channel.send('You do not have any lootboxes right now. Earn XP and Level Up to earn more!')
        return
    
    final_string = '**YOUR LOOTBOXES:**\n'
    for box in user_lootboxes:
        final_string += '📦 **Level '+str(box)+" Lootbox:** - To open, use the command **!open "+str(box)+"**\n"
    for _ in range(twitch_lootboxes):
        final_string += "🟣 **Twitch Sub Lootbox:** - To open, use the command **!open twitch**"

    await message.channel.send(final_string)
    

