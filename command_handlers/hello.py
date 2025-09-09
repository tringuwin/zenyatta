import random

from safe_send import safe_send

async def hello_handler(message):
    answers = [
        'Greetings.',
        'Hello.',
        'I greet you.',
        'Peace be upon you.'
    ]

    random_response = random.choice(answers)
    await safe_send(message.channel, random_response)