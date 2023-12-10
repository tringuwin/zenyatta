
async def not_registered_response(message):
    await message.channel.send(message.author.mention+" It seems like you're not registered yet. Use this command to register: **!battle YourBattleTagHere#1234**")

async def invalid_number_of_params(message):
    await message.channel.send("Invalid number of parameters. Please check **!help** for more details.")