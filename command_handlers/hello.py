import random

async def hello_handler(message):
    answers = [
        'Greetings.',
        'Hello.',
        'I greet you.',
        'Peace be upon you.'
    ]

    random_response = random.choice(answers)
    print('sending response')
    await message.channel.send(random_response)