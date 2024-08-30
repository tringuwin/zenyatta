
from league import validate_admin
import uuid
import time
import discord

async def set_lineup_handler(db, message):

    valid_admin, _, team_name, _ = await validate_admin(db, message)

    if message.author.id == 1112204092723441724:
        valid_admin = True
        team_name = 'Polar'

    if not valid_admin:
        await message.channel.send('You are not an admin of a league team.')
        return
    
    random_uuid_string = str(uuid.uuid4())
    
    lineup_tokens = db['lineup_tokens']
    current_lineup_token = lineup_tokens.find_one({'discord_id': message.author.id})

    if current_lineup_token:
        lineup_tokens.update_one({'discord_id': message.author.id}, {'$set': {'token': random_uuid_string, 'created': time.time(), 'team_name': team_name}})
    else:
        new_token = {
            'token': random_uuid_string,
            'discord_id': message.author.id,
            'team_name': team_name,
            'created': time.time()
        }
        lineup_tokens.insert_one(new_token)
    
    try:
        await message.author.send(f'Use this link to edit the lineup for {team_name}: https://spicyragu.netlify.app/sol/lineup/{random_uuid_string}\n\nDO NOT SHARE THIS LINK WITH ANYONE')
        await message.channel.send('A link to edit the lineup for '+team_name+' was sent to your DMs.')
    except discord.Forbidden:
        await message.channel.send('I tried to DM you a private link to edit the lineup for your team, but your privacy settings did not allow me to. Please check your privacy settings and try again.')