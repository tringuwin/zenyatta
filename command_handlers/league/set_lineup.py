
from context.context_helpers import get_league_url_from_context
from league import validate_admin
import uuid
import time
import discord
import constants
from safe_send import safe_dm, safe_send

async def set_lineup_handler(db, message, context):

    valid_admin, _, team_name, _ = await validate_admin(db, message, context)

    if message.author.id == constants.SPICY_RAGU_ID:
        valid_admin = True
        team_name = 'Ragu'

    if not valid_admin:
        await safe_send(message.channel, 'You are not an admin of a league team.')
        return
    
    random_uuid_string = str(uuid.uuid4())
    
    lineup_tokens = db['lineup_tokens']
    current_lineup_token = lineup_tokens.find_one({'discord_id': message.author.id, 'context': context, 'team_name': team_name})

    if current_lineup_token:
        lineup_tokens.update_one({'discord_id': message.author.id}, {'$set': {'token': random_uuid_string, 'created': time.time(), 'team_name': team_name, 'context': context}})
    else:
        new_token = {
            'token': random_uuid_string,
            'discord_id': message.author.id,
            'team_name': team_name,
            'created': time.time(),
            'context': context
        }
        lineup_tokens.insert_one(new_token)
    
    try:
        league_url = get_league_url_from_context(context)
        await safe_dm(message.author, (f'Use this link to edit the lineup for {team_name}: {constants.WEBSITE_DOMAIN}/{league_url}/lineup/{random_uuid_string}\n\nDO NOT SHARE THIS LINK WITH ANYONE'))
        await safe_send(message.channel, 'A link to edit the lineup for '+team_name+' was sent to your DMs.')
    except discord.Forbidden:
        await safe_send(message.channel, 'I tried to DM you a private link to edit the lineup for your team, but your privacy settings did not allow me to. Please check your privacy settings and try again.')