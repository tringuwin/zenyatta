import discord

async def help_lft_handler(message):

    help_embed = discord.Embed(title='List of LFT (looking for team) commands:')
    help_embed.add_field(name='!LFT', value="Get a link to a list of players looking to join a League Team.", inline=False)
    help_embed.add_field(name='!toggleLFT', value="Turn on/off if you're looking for a team. Will be displayed on the website if you're looking for a team.", inline=False)
    help_embed.add_field(name='!updateLFT', value="Updates your LFT profile if it's showing old data.", inline=False)
    help_embed.add_field(name='!setLFTcolor [hex code]', value="Set the background color for your LFT profile.", inline=False)
    help_embed.add_field(name='!setLFTHero [number 1-4] [hero name]', value="Set the heroes you play on your profile. There are 4 spots available.", inline=False)
    help_embed.add_field(name='!bumpLFT', value="Make your profile appear at the top of the list for a higher chance of being noticed!", inline=False)

    await message.channel.send(embed=help_embed)