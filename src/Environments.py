from Environment import Environment

environments = [

    Environment(
        name="Grand Bazaar Market",
        description="A lively market where merchants haggle and buyers gossip.",
        max_turns=6,
        message_length_limit=12,
        forbidden_words=["spy", "agent", "secret"],
        # noise_chance=0.15
    ),

    Environment(
        name="Opera House Balcony",
        description="Secrets whispered in velvet shadows above the stage.",
        max_turns=5,
        message_length_limit=15,
        forbidden_words=["plot", "assassinate"],
        # noise_chance=0.1
    ),

    Environment(
        name="Luxury Train Dining Car",
        description="Elegant meals served as landscapes blur by the windows.",
        max_turns=8,
        message_length_limit=10,
        forbidden_words=["escape", "attack"],
        # noise_chance=0.05
    ),

    Environment(
        name="Seaside Boardwalk",
        description="Waves crash as children laugh and vendors shout.",
        max_turns=7,
        message_length_limit=14,
        forbidden_words=["drop", "dead"],
        # noise_chance=0.2
    ),

    Environment(
        name="Mountain Lodge",
        description="Crackling fireplaces conceal whispers over hot drinks.",
        max_turns=6,
        message_length_limit=16,
        forbidden_words=["fire", "bomb"],
        # noise_chance=0.05
    ),

    Environment(
        name="Rooftop Garden",
        description="Hidden among vines and lanterns, a breeze carries words away.",
        max_turns=5,
        message_length_limit=12,
        forbidden_words=["escape", "climb"],
        # noise_chance=0.25
    ),

    Environment(
        name="Underground Jazz Club",
        description="Smoke and saxophones drown out secrets in the dim haze.",
        max_turns=7,
        message_length_limit=15,
        forbidden_words=["kill", "gun"],
        # noise_chance=0.3
    ),

    Environment(
        name="Old Library",
        description="Whispers drift through aisles of forgotten tomes.",
        max_turns=6,
        message_length_limit=20,
        forbidden_words=["burn", "explode"],
        # noise_chance=0.05
    ),

    Environment(
        name="Desert Caravan Camp",
        description="Stars glimmer as firelight flickers across tired travelers.",
        max_turns=8,
        message_length_limit=14,
        forbidden_words=["sandstorm", "ambush"],
        # noise_chance=0.15
    ),

    Environment(
        name="Art Museum Gallery",
        description="Silent guards watch as visitors admire timeless works.",
        max_turns=6,
        message_length_limit=12,
        forbidden_words=["steal", "painting"],
        # noise_chance=0.1
    ),

    Environment(
        name="Harbor Dockside",
        description="Fog clings to crates while sailors trade shouts and smokes.",
        max_turns=7,
        message_length_limit=10,
        forbidden_words=["ship", "cargo"],
        # noise_chance=0.2
    ),

    Environment(
        name="Snowbound Train Station",
        description="Travelers huddle in coats as snow buries the tracks.",
        max_turns=8,
        message_length_limit=15,
        forbidden_words=["train", "delay"],
        # noise_chance=0.1
    ),
]