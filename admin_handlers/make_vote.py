
import constants
from discord_actions import get_guild
from helpers import get_constant_value, set_constant_value
from safe_send import safe_send


async def make_vote_handler(db, message, client):

    current_vote = get_constant_value(db, 'sub_vote')
    if current_vote['active']:
        await safe_send(message.channel, 'There is currently an active vote. End that one before starting a new one.')
        return

    message_parts = message.content.split('|')
    if len(message_parts) < 4:
        await safe_send(message.channel, 'Invalid number of params.')
        return
    
    message_parts.pop(0)
    title = message_parts.pop(0)
    upper_title = title.upper()

    final_string = '**'+upper_title+':**'
    index = 1
    options = []
    for message_part in message_parts:
        final_string += '\n'+str(index)+'. '+message_part+' : **0 VOTES** | use **!vote '+str(index)+'** to vote'

        options.append({
            'name': message_part,
            'votes': 0
        })

        index += 1

    guild = await get_guild(client)
    sub_vote_channel = guild.get_channel(constants.SUB_VOTE_CHANNEL)
    await safe_send(sub_vote_channel, '<@&1273403775024894062>', True)
    vote_msg = await safe_send(sub_vote_channel, final_string)

    current_vote['active'] = True
    current_vote['title'] = upper_title
    current_vote['options'] = options
    current_vote['voted_users'] = []
    current_vote['vote_msg_id'] = vote_msg.id

    set_constant_value(db, 'sub_vote', current_vote)

    await safe_send(message.channel, 'Vote started')


