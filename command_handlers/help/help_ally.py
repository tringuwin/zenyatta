import discord

from safe_send import safe_add_field, safe_create_embed, safe_send_embed

async def help_ally_handler(message):

    help_embed = safe_create_embed('List of commands related to League Team Allies and Rivals:')

    safe_add_field(help_embed, '!allyrequest [team name here]', 'Send an Ally Request from your League Team to another League Team.', False)
    safe_add_field(help_embed, '!rivalrequest [team name here]', 'Send a Rival Request from your League Team to another League Team.', False)
    safe_add_field(help_embed, '!acceptally [team name here]', 'Accept an Ally Request from another League Team.', False)
    safe_add_field(help_embed, '!acceptrival [team name here]', 'Accept a Rival Request from another League Team.', False)
    safe_add_field(help_embed, '!allyrequests', 'Check all the Ally Requests your team has received from other League Teams.', False)
    safe_add_field(help_embed, '!rivalrequests', 'Check all the Rival Requests your team has received from other League Teams.', False)
    safe_add_field(help_embed, '!delally [team name here]', 'Remove an Ally from your League Team.', False)
    safe_add_field(help_embed, '!delrival [team name here]', 'Remove a Rival from your League Team.', False)
    safe_add_field(help_embed, '!denyally [team name here]', 'Deny an Ally Request from another League Team.', False)
    safe_add_field(help_embed, '!denyrival [team name here]', 'Deny a Rival Request from another League Team.', False)
    safe_add_field(help_embed, '!cancelally [team name here]', 'Cancel an Ally Request to another League Team.', False)
    safe_add_field(help_embed, '!cancelrival [team name here]', 'Cancel a Rival Request to another League Team.', False)

    await safe_send_embed(message.channel, help_embed)