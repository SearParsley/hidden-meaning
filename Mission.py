class Mission:
    """Defines the mission parameters for the game."""

    def __init__(self, objective: str, environment: str, forbidden_words: list[str]):
        self.objective = objective
        self.environment = environment
        self.forbidden_words = forbidden_words