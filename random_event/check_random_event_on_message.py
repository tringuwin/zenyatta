import random

from random_event.random_event import try_random_event

async def check_random_event_on_message(db, client):
    
    random_event_chance = random.randint(1, 100)
    if random_event_chance == 100:
        await try_random_event(db, client)