

async def send_msg(channel, info, source):
    print('Message from source: '+source)
    await channel.send(info)