import discord

from safe_send import safe_send_embed

async def help_ally_handler(message):

    help_embed = discord.Embed(title='List of commands related to League Team Allies and Rivals:')
    help_embed.add_field(name='!allyrequest [team name here]', value='Send an Ally Request from your League Team to another League Team.', inline=False)
    help_embed.add_field(name='!rivalrequest [team name here]', value='Send a Rival Request from your League Team to another League Team.', inline=False)
    help_embed.add_field(name='!acceptally [team name here]', value='Accept an Ally Request from another League Team.', inline=False)
    help_embed.add_field(name='!acceptrival [team name here]', value='Accept a Rival Request from another League Team.', inline=False)
    help_embed.add_field(name='!allyrequests', value='Check all the Ally Requests your team has received from other League Teams.', inline=False)
    help_embed.add_field(name='!rivalrequests', value='Check all the Ally Requests your team has received from other League Teams.', inline=False)
    help_embed.add_field(name='!delally [team name here]', value='Remove an Ally from your League Team.', inline=False)
    help_embed.add_field(name='!delrival [team name here]', value='Remove a Rival from your League Team.', inline=False)
    help_embed.add_field(name='!denyally [team name here]', value='Deny an Ally Request from another League Team.', inline=False)
    help_embed.add_field(name='!denyrival [team name here]', value='Deny a Rival Request from another League Team.', inline=False)
    help_embed.add_field(name='!cancelally [team name here]', value='Cancel an Ally Request to another League Team.', inline=False)
    help_embed.add_field(name='!cancelrival [team name here]', value='Cancel a Rival Request to another League Team.', inline=False)

    await safe_send_embed(message.channel, help_embed)