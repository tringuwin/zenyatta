import random

MAPS = [

    [ # Control
        'Busan', 
        'Nepal',
        'Ilios',
        'Oasis',
        'Lijang Tower',
        'Antarctic Peninsula',
        'Samoa'
    ],
    [ # Escort
        'Circuit Royal',
        'Dorado',
        'Route 66',
        'Junkertown',
        'Rialto',
        'Havana',
        'Watchpoint: Gibraltar',
        'Shambali Monastery'
    ],
    [ # Hybrid
        'Blizzard World',
        'Numbani',
        'Hollywood',
        'Eichenwalde',
        "King's Row",
        'Midtown',
        'Paraiso'
    ],
    [ # Push
        'Colosseo',
        'Esperanca',
        'New Queen Street',
        'Runasapi'
    ],
    [ # Flashpoint
        'New Junk City',
        'Survasa'
    ],
    [ # Clash
        'Hanaoka',
        'Throne of Anubis'
    ]

]

async def random_map_handler(message):

    game_mode = random.choice(MAPS)
    map = random.choice(game_mode)

    await message.channel.send(map)