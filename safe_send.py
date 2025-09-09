
import discord

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
    return await channel.send(cleaned_text)


async def safe_reply(message, text, can_ping_role=False):

    cleaned_text = clean_text(text, can_ping_role=can_ping_role)
    await message.reply(cleaned_text)


async def safe_dm(user, text):

    # no need to clean text for dms
    await user.send(text)


# NOT IMPLEMENTED YET
async def safe_edit():

    pass


# NOT REPLACED EVERYWHERE YET
def safe_create_embed(title):

    safe_title = clean_text(title)

    return discord.Embed(title=safe_title)


# NOT REPLACED EVERYWHERE YET
def safe_add_field(embed, name, value, inline):

    safe_name = clean_text(name)
    safe_value = clean_text(value)

    embed.add_field(name=safe_name, value=safe_value, inline=inline)


# NOT REPLACED EVERYWHERE YET
def safe_set_footer(embed, text, icon_url):

    safe_text = clean_text(text)

    embed.set_footer(text=safe_text, icon_url=icon_url)


async def safe_send_embed(channel, embed):

    # have to check embed content earlier
    return await channel.send(embed=embed)


async def safe_send_multiple_embeds(channel, embeds):

    # have to check embed content earlier
    return await channel.send(embeds=embeds)



# NOT IMPLEMENTED YET
async def safe_edit_embed():

    pass