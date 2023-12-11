

async def send_msg(channel, info, source):
    print('Message from source: '+source)
    await channel.send(info)


async def give_role(member, role, source):
    print('Role add from source: '+source)
    await member.add_roles(role)

async def give_many_roles(member, role_array):
    print('')


async def get_member(guild, user_id, source):
    print('Get member from source: '+source)
    return guild.get_member(user_id)
