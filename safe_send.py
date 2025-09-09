
import discord

def clean_possible_role_pings(text):

    text = text.replace('@&', ' @ & ')
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


async def safe_edit(message, text):

    cleaned_text = clean_text(text)
    await message.edit(content=cleaned_text)


def safe_create_embed(title, description=None, color=None):

    safe_title = clean_text(title)
    safe_description = clean_text(description) if description else None

    return discord.Embed(title=safe_title, description=safe_description, color=color)


def safe_add_field(embed, name, value, inline):

    safe_name = clean_text(name)
    safe_value = clean_text(value)

    embed.add_field(name=safe_name, value=safe_value, inline=inline)


def safe_set_footer(embed, text, icon_url=None):

    safe_text = clean_text(text)

    embed.set_footer(text=safe_text, icon_url=icon_url)


async def safe_send_embed(channel, embed):

    # have to check embed content earlier
    return await channel.send(embed=embed)


async def safe_send_multiple_embeds(channel, embeds):

    # have to check embed content earlier
    return await channel.send(embeds=embeds)


async def safe_edit_embed(message, embed):

    await message.edit(embed=embed, content='')


async def safe_send_test(message):

    await safe_send(message.channel, '@everyone @here /everyone /here @&RoleName')