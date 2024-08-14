

async def make_vote_handler(db, message, client):

    message_parts = message.content.split('|')
    if len(message_parts) < 4:
        await message.channel.send('Invalid number of params.')
        return
    
    message_parts.pop(0)
    title = message_parts.pop(0)
    upper_title = title.upper()


    final_string = f'{upper_title}:'
    index = 1
    for message_part in message_parts:
        final_string += '\n'+str(index)+'. '+message_part
        index += 1

    await message.channel.send(final_string)


