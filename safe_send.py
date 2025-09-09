


def clean_possible_role_pings(text):

    text = text.replace('@&', ' @& ')
    return text


def clean_text(text, can_ping_role=False):
    
    if not can_ping_role:
        text = clean_possible_role_pings(text)

    text = text.replace('@everyone', '@ everyone')
    text = text.replace('@here', '@ here')
    text = text.replace('/everyone', '/ everyone')
    text = text.replace('/here', '/ here')

    return text


async def safe_send(channel, text, can_ping_role=False):

    cleaned_text = clean_text(text, can_ping_role=can_ping_role)
    await channel.send(cleaned_text)


async def safe_reply(message, text, can_ping_role=False):

    cleaned_text = clean_text(text, can_ping_role=can_ping_role)
    await message.reply(cleaned_text)


async def safe_dm(user, text):

    # no need to clean text for dms
    await user.send(text)