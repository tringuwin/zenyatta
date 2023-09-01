
async def not_registered_response(message):
    await message.channel.send("It seems like you're not registered yet. Use this command to register: **!battle YourTagHere#1234**")

async def invalid_number_of_params(message):
    await message.channel.send("Invalid number of parameters.")