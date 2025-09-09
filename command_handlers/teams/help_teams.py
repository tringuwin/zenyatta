
from safe_send import safe_create_embed, safe_send_embed, safe_add_field

async def help_teams_handler(message):

    help_embed = safe_create_embed('List of teams commands:')

    safe_add_field(help_embed, '!teams', 'See the teams that you are currently part of.', False)
    safe_add_field(help_embed, '!teaminfo [team name]', 'See the details of a specific team.', False)
    safe_add_field(help_embed, '!maketeam [team size] [team name]', 'Make a new team.', False)
    safe_add_field(help_embed, '!invite [@player] [team name]', 'Invite a user to a team you own by mentioning them.', False)
    safe_add_field(help_embed, '!myinvites', 'See a list of teams you are invited to.', False)
    safe_add_field(help_embed, '!acceptinvite [team name]', 'Accept an invite to a team.', False)
    safe_add_field(help_embed, '!denyinvite [team name]', 'Deny an invite to a team.', False)
    safe_add_field(help_embed, '!teamjoin [event id] [team name]', 'Join an event as a team.', False)
    safe_add_field(help_embed, '!leaveteam [team name]', 'Leave a team.', False)
    safe_add_field(help_embed, '!deleteteam [team name]', 'Delete a team you own.', False)
    safe_add_field(help_embed, '!kickplayer [@player] [team name]', 'Kick a player from a team you own.', False)

    await safe_send_embed(message.channel, help_embed)