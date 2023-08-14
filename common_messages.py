
async def not_registered_response(message):
    await message.channel.send("It seems like you're not registered yet. Please register first.")

async def invalid_number_of_params(message):
    await message.channel.send("Invalid number of parameters.")