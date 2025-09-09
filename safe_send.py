


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



