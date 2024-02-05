
async def not_registered_response(message):
    await message.channel.send(message.author.mention+" It seems like you're not registered yet. Please go to this channel ( https://discord.com/channels/1130553449491210442/1130553489106411591 ) and use this command to register: **!battle YourBattleTagHere#1234**")

async def invalid_number_of_params(message):
    await message.channel.send("Invalid number of parameters. Please check **!help** for more details.")