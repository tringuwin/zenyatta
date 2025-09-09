import random

from safe_send import safe_send

OVERWATCH_MAPS = [

    [ # Control
        'Busan', 
        'Nepal',
        'Ilios',
        'Oasis',
        'Lijiang Tower',
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
        'Suravasa'
    ],
    # [ # Clash
    #     'Hanaoka',
    #     'Throne of Anubis'
    # ]

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

def get_random_map(context):

    if context not in CONTEXT_TO_MAPS:
        return "NO_MAP"
    
    possible_maps = CONTEXT_TO_MAPS[context]

    game_mode = random.choice(possible_maps)
    map = random.choice(game_mode)

    return map


async def random_map_handler(message, context):

    if context not in CONTEXT_TO_MAPS:
        await safe_send(message.channel, "There are no maps for this league yet.")
        return
    
    random_map = get_random_map(context)

    await safe_send(message.channel, random_map)