
from common_messages import invalid_number_of_params
import constants
from discord_actions import get_message_by_channel_and_id, get_role_by_id
from helpers import can_be_int, get_constant_value, set_constant_value, valid_number_of_params
from safe_send import safe_send

async def update_vote(client, current_vote):

    final_string = '**'+current_vote['title']+':**'
    index = 1
    for option in current_vote['options']:
        final_string += '\n'+str(index)+'. '+option['name']+' : **'+str(option['votes'])+' VOTES** | use **!vote '+str(index)+'** to vote'
        index += 1

    vote_message = await get_message_by_channel_and_id(client, constants.SUB_VOTE_CHANNEL, current_vote['vote_msg_id'])
    await vote_message.edit(content=final_string)

async def vote_handler(db, message, client):

    twitch_sub_role = await get_role_by_id(client, constants.TWITCH_SUB_ROLE)
    if not twitch_sub_role in message.author.roles:
        await safe_send(message.channel, 'Only Twitch Subscribers are able to vote.')
        return
    
    current_vote = get_constant_value(db, 'sub_vote')
    if not current_vote['active']:
        await safe_send(message.channel, 'There is no vote at the moment.')
        return

    if message.author.id in current_vote['voted_users']:
        await safe_send(message.channel, 'You have already voted in this vote.')
        return

    valid_params, params = valid_number_of_params(message, 2)
    if not valid_params:
        await invalid_number_of_params(message)
        return
    
    vote_option = params[1]

    if not can_be_int(vote_option):
        await safe_send(message.channel, vote_option+' is not a valid number.')
        return
    vote_option = int(vote_option)
    
    num_options = len(current_vote['options'])
    if (vote_option < 0) or vote_option > num_options:
        await safe_send(message.channel, 'That number is not a valid option for this vote.')
        return
    
    actual_index = vote_option - 1
    current_vote['options'][actual_index]['votes'] +=1
    current_vote['voted_users'].append(message.author.id)

    set_constant_value(db, 'sub_vote', current_vote)

    await safe_send(message.channel, 'You successfully voted for option '+str(vote_option)+'!')
    await update_vote(client, current_vote)
    


