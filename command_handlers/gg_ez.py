import random

responses = [
    'Well played. I salute you all.',
    'For glory and honor! Huzzah comrades!',
    "I'm wrestling with some insecurity issues in my life but thank you all for playing with me.",
    "It's past my bedtime. Please don't tell my mommy.",
    'Gee whiz! That was fun. Good playing!',
    'I feel very, very small... please hold me...'
]

async def gg_ez_handler(message):

    my_response = random.choice(responses)
    await message.channel.send(my_response)