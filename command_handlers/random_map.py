import random

OVERWATCH_MAPS = [

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

MARVEL_RIVALS_MAPS = [

    [ # Convergence
        'Central Park',
        'Hall of Djalia',
        'Symbiotic Surface',
        'Shin-Shibuya',
    ],

    [ # Convoy
        'Midtown',
        'Spider-Islands',
        'Yggdrasill Path'
    ],

    [ # Domination
        "Hell's Heaven",
        "Birnin T'Challa",
        'Royal Palace',
    ]

]

CONTEXT_TO_MAPS = {
    'OW': OVERWATCH_MAPS,
    'MR': MARVEL_RIVALS_MAPS
}

async def random_map_handler(message, context):

    if context not in CONTEXT_TO_MAPS:
        await message.channel.send("There are no maps for this league yet.")
        return
    
    possible_maps = CONTEXT_TO_MAPS[context]

    game_mode = random.choice(possible_maps)
    map = random.choice(game_mode)

    await message.channel.send(map)